import time

import transform
from exporter import Exporter
import json
import unittest
from pathlib import Path

home = Path.home()

with open(f"{home}/ariatest.json", "r") as config_file:
    config = json.load(config_file)
    url = config["url"]
    username = config["username"]
    password = config["password"]

exporter = Exporter(url, username, password, None, True)

class TestClient(unittest.TestCase):
    def test_simple(self):
        data = exporter.export(
            { "resourceKind": [ "HostSystem" ]},
            ["cpu|demandmhz", "cpu|demandpct"],
            time.time() - 86400,
            time.time())
        print(data)
        t_data = transform.to_simple_table(exporter, data)
        print(t_data)

    def test_chunked(self):
        chunks = exporter.export_chunked(
            {"resourceKind": ["VirtualMachine"]},
            ["cpu|demandmhz", "cpu|demandpct"],
            time.time() - 900,
            time.time(), chunk_size=1000)
        for chunk in chunks:
            print(transform.to_simple_table(exporter, chunk))


