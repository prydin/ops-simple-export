import time
from time import strftime

import transform
from exporter import Exporter
import json
from datetime import datetime
from pathlib import Path

from exporter_test import exporter

# Load the config file
home = Path.home()
with open(f"{home}/ariatest.json", "r") as config_file:
    config = json.load(config_file)
    url = config["url"]
    username = config["username"]
    password = config["password"]

# Query parameters
metrics = ["cpu|demandpct", "cpu|demandmhz"]
lookback = 900 # 900s = 15 minutes
start = time.time() - lookback
end = time.time()
resource_query = { "name": [ "Nginx" ]}

# Run query
e = Exporter(url, username, password, None, True)
result = e.export(resource_query, metrics, start, end, "AVG", 5)

# Print result
table = transform.to_simple_table(e, result)
for resource in table:
    print(resource["resourceName"])
    for metrics in resource["metrics"]:
        print(f"  {metrics['metric_name']}")
        for value in metrics["values"]:
            ts = int(value['timestamp']) / 1000
            print(f"    {datetime.fromtimestamp(ts)} -> {value['value']}")
