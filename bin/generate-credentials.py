#!/usr/bin/env python3

import pathlib
import sys
import pprint

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from peplink_api.services import PepLinkRawService


host_name = input("Enter the PepLink router's hostname: ")
client_name = input("Enter client name (description): ")
username = input("Username: ")
password = input("Password: ")
url = f"https://{host_name}/"
raw_service = PepLinkRawService(url=url)
raw_service.password_login(username=username, password=password)

for client in raw_service.list_clients():
    if client["name"] == client_name:
        print("Found existing client")
        break
else:
    print("Createing test client")
    client = raw_service.create_client(name=client_name)
pprint.pprint(client)
