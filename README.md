# A simple wrapper for the VCF Operations API

This small wrapper is aimed at simplifying metric retrieval from VCF Opertions.

## Example
```python
import time

import transform
from exporter import Exporter
from datetime import datetime

# Query parameters
metrics = ["cpu|demandpct", "cpu|demandmhz"]
lookback = 900 # 900s = 15 minutes
start = time.time() - lookback
end = time.time()
resource_query = { "name": [ "Nginx" ]}

# Run query
e = Exporter("https://myops.com", "me", "mypassword", None, True)
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

```

Result: 
```text
Nginx_512MB_107
  cpu|demandmhz
    2025-05-05 16:24:59.999000 -> 10.600000381469727
    2025-05-05 16:29:59.999000 -> 10.733333587646484
    2025-05-05 16:34:59.999000 -> 10.399999618530273
  cpu|demandPct
    2025-05-05 16:24:59.999000 -> 0.5059477686882019
    2025-05-05 16:29:59.999000 -> 0.5123118758201599
    2025-05-05 16:34:59.999000 -> 0.4964015781879425
Nginx-Nxt4-500-175
  cpu|demandmhz
    2025-05-05 16:24:59.999000 -> 74.80000305175781
    2025-05-05 16:29:59.999000 -> 47.93333435058594
    2025-05-05 16:34:59.999000 -> 52.599998474121094
  cpu|demandPct
    2025-05-05 16:24:59.999000 -> 3.5702731609344482
    2025-05-05 16:29:59.999000 -> 2.287902355194092
    2025-05-05 16:34:59.999000 -> 2.5106465816497803
```