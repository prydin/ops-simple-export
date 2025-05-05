import requests

class Client:
    headers = { "Accept": "application/json", "Content-Type": "application/json"}

    id_to_name_cache = {}

    url_base = ""
    verify = True
    session = None

    def __init__(self, url, ignore_validate = False):
        self.url_base = url + "/suite-api/api"
        self.verify = not ignore_validate
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def get(self, uri):
        result = self.session.get(self.url_base + uri, verify=self.verify, headers=self.headers)
        if result.status_code not in range(200,299):
            raise Exception(f"API Error: {result.status_code}: {result.content}")
        return result.json()

    def post(self, uri, payload):
        result = self.session.post(self.url_base + uri, json=payload, verify=self.verify, headers=self.headers)
        if result.status_code not in range(200,299):
            raise Exception(f"API Error: {result.status_code}: {result.content}")
        return result.json()

    def login(self, username, password, auth_source):
        payload = {
            "username": username,
            "password": password,
            "authSource": auth_source,
        }
        result = self.post("/auth/token/acquire", payload)
        token = result["token"]
        self.headers["Authorization"] = "OpsToken " + token
        self.session.headers.update(self.headers)

    def query_resources(self, query, page_size = 1000, page = 0):
        result = self.post(f"/resources/query?pageSize={page_size}&page={page}", query)
        resources = result["resourceList"]

        # Load name cache
        for resource in resources:
            self.id_to_name_cache[resource["identifier"]] = resource["resourceKey"]["name"]
        return resources

    def get_cached_resource_name(self, id):
        return self.id_to_name_cache.get(id, None)

    def query_metrics(self, resources, metrics, start, end, rollup_type = "AVG", rollup_minutes = 5):
        resource_ids = list(map(lambda r: r["identifier"], resources))
        payload = {
            "resourceId": resource_ids,
            "statKey": metrics,
            "begin": int(start*1000),
            "end": int(end*1000),
            "intervalType": "MINUTES",
            "rollUpType": rollup_type,
            "rollUpQuantifier": rollup_minutes
        }
        result = self.post("/resources/stats/query", payload)["values"]

        # Remove unnecessary nodes
        for resource_metrics in result:
            resource_metrics["stats"] = resource_metrics["stat-list"]["stat"]
            del resource_metrics["stat-list"]
        return result
