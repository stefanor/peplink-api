import datetime
import urllib.parse
from time import mktime
from typing import Optional

from demands import HTTPServiceClient


class PepLinkRawService(HTTPServiceClient):
    """Lower level API client, that doesn't handle auth details

    API methods will be authenticated after calling password_login(), by cookie
    """

    def __init__(self, url, verify=False):
        super().__init__(url)
        self.verify = verify  # By default we'll get an unverifyable certificate

    def is_acceptable(self, response, request_params) -> bool:
        if not super().is_acceptable(response, request_params):
            return False
        return response.json()["stat"] == "ok"

    def password_login(self, username, password):
        return self.post(
            "/api/login", data={"username": username, "password": password}
        ).json()["response"]

    def client_login(self, client_id, client_secret):
        return self.post(
            "/api/auth.token.grant",
            data={"clientId": client_id, "clientSecret": client_secret},
        ).json()["response"]

    def create_client(self, name, scope="api.read-only"):
        return self.post(
            "/api/auth.client", data={"action": "add", "name": name, "scope": scope}
        ).json()["response"]

    def delete_client(self, client_id):
        return self.post(
            "/api/auth.client", data={"action": "remove", "clientId": client_id}
        ).json()

    def list_clients(self):
        # Requires RW admin credentials
        return self.get("/api/auth.client").json()["response"]

    def ap_status(self):
        return self.get("/api/cmd.ap").json()["response"]

    def carrier_scan(self, conn_id):
        return self.get(
            "/api/cmd.carrier.scan", params={"connId": conn_id, "reference": "yes"}
        ).json()["response"]

    def wan_status(self, conn_ids=None):
        params = {}
        if isinstance(conn_ids, list):
            params["id"] = ",".join(str(x) for x in conn_ids)
        elif isinstance(conn_ids, int):
            params["id"] = [str(conn_ids)]
        return self.get("/api/status.wan.connection", params=params).json()["response"]

    def client_status(self, weight="normal"):
        return self.get("/api/status.client", params={"outputWeight": weight}).json()[
            "response"
        ]

    def client_bandwidth_usage(
        self,
        from_: datetime.datetime,
        to: Optional[datetime.datetime] = None,
        period="daily",
    ):
        """
        Counters appear to be updated ~1/minute
        """
        if to is None:
            to = datetime.datetime.now()
        return self.get(
            "/api/status.bandwidthUsage.client",
            params={
                "period": period,
                "from": int(mktime(from_.timetuple())),
                "to": int(mktime(to.timetuple())),
            },
        ).json()["response"]


class PepLinkClientService(PepLinkRawService):
    """API client that supports Client ID & Client Secret authentication"""

    client_id: str
    client_secret: str
    access_token: Optional[str]
    access_token_expiry: Optional[datetime.datetime]

    def __init__(self, url, client_id, client_secret, verify=False):
        super().__init__(url, verify)
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_expiry = None

    def pre_send(self, request_params):
        if not self.access_token or self.access_token_expiry <= datetime.datetime.now():
            r = PepLinkRawService(self.url).client_login(
                self.client_id, self.client_secret
            )
            self.access_token = r["accessToken"]
            self.access_token_expiry = datetime.datetime.now() + datetime.timedelta(
                seconds=r["expiresIn"] - 5
            )
        url = urllib.parse.urlparse(request_params["url"])
        querydict = urllib.parse.parse_qs(url.query)
        querydict["accessToken"] = self.access_token
        query = urllib.parse.urlencode(querydict)
        request_params["url"] = urllib.parse.urlunparse(url._replace(query=query))
        return super().pre_send(request_params)
