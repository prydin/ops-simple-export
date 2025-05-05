import json
import unittest
from client import Client

with open("/Users/pontusrydin/ariatest.json", "r") as config_file:
    config = json.load(config_file)
    url = config["url"]
    username = config["username"]
    password = config["password"]

client = Client(url, True)

class TestClient(unittest.TestCase):
    def login(self):
        client.login(username, password, None)

    def test_login(self):
        self.login()

    def test_get_host_resources(self):
        self.login()
        resources = client.query_resources({ "resourceKind": [ "HostSystem" ]})
        assert len(resources) > 0

