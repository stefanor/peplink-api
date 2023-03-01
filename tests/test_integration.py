import datetime
import errno
import json
import time
from unittest import TestCase, SkipTest

from peplink_api.services import PepLinkClientService, PepLinkRawService


class FunctionalIntegrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            with open("credentials.json") as f:
                cls.credentials = json.load(f)
        except IOError as e:
            if e.errno == errno.ENOENT:
                raise SkipTest("No integration test credentials provided")
            raise
        cls.raw_service = PepLinkRawService(cls.credentials["url"])
        cls.service = PepLinkClientService(
            cls.credentials["url"],
            cls.credentials["client_id"],
            cls.credentials["client_secret"],
        )

    def test_create_credentials(self):
        self.raw_service.password_login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        client = self.raw_service.create_client(
            name="Functional Integration Test: test_create_credentials"
        )
        self.addCleanup(self.raw_service.delete_client, client["clientId"])
        time.sleep(1)  # We're rate-limited
        self.assertTrue(
            self.raw_service.client_login(client["clientId"], client["clientSecret"])
        )

    def test_carrier_scan(self):
        self.assertIn("scanStatus", self.service.carrier_scan(2))

    def test_wan_status(self):
        self.assertIn("order", self.service.wan_status())

    def test_list_clients(self):
        self.raw_service.password_login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        for client in self.raw_service.list_clients():
            if client["name"] == "peplink_api Functional Integration Test":
                self.assertEqual(client["clientId"], self.credentials["client_id"])
                self.assertEqual(
                    client["clientSecret"], self.credentials["client_secret"]
                )
                break
        else:
            self.assertFalse("Test client not found")

    def test_client_status(self):
        self.assertIn("list", self.service.client_status())

    def test_client_bandwidth_usage(self):
        month_start = datetime.datetime.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        self.assertIn(
            "monthly",
            self.service.client_bandwidth_usage(period="monthly", from_=month_start),
        )

    def test_time_config(self):
        time = self.service.time_config()
        self.assertIn("timeZone", time)
        self.assertIn("syncSource", time)
        self.assertIn("timeServer", time)
        self.assertIn("defaultTimeServer", time)
        self.assertIn("timeZoneList", time)
        self.assertIn("timeDst", time)
        for zone in time["timeZoneList"]:
            self.assertIn("name", zone)
            self.assertIn("value", zone)
            self.assertIn("offset", zone)

    def test_traffic_status(self):
        self.assertIn("bandwidth", self.service.traffic_status())
