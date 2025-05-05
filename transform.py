def to_simple_table(exporter, input):
    result = []
    for resource in input:
        res_name = exporter.get_resource_name(resource["resourceId"])
        metrics_result = []
        resource_result = {
            "resourceName": res_name,
            "metrics": metrics_result
        }
        result.append(resource_result)
        for stat in resource["stats"]:
            value_result = []
            metric_result = {
                "metric_name": stat["statKey"]["key"],
                "values": value_result
            }
            metrics_result.append(metric_result)
            values = stat["data"]

            for i, ts in enumerate(stat["timestamps"]):
                value_result.append({"timestamp": ts, "value": values[i]})
    return result


