#!/usr/bin/env python3

import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from peplink_api.services import PepLinkRawService

CLIENT_NAME = "peplink_api Functional Integration Test"

host_name = input("Enter the PepLink router's hostname: ")
username = input("Username: ")
password = input("Password: ")
credentials = {
    "url": f"https://{host_name}/",
    "username": username,
    "password": password,
}
raw_service = PepLinkRawService(url=credentials["url"])
raw_service.password_login(username=username, password=password)

for client in raw_service.list_clients():
    if client["name"] == CLIENT_NAME:
        print("Found existing client")
        break
else:
    print("Createing test client")
    client = raw_service.create_client(name=CLIENT_NAME)
credentials["client_id"] = client["clientId"]
credentials["client_secret"] = client["clientSecret"]

os.umask(0o077)
with open("credentials.json", "w") as f:
    json.dump(credentials, f, indent=2)
    f.write("\n")
