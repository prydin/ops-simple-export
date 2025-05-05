from client import Client

class Cursor:
    """
    A class used to iterate over chunks of resources and their metrics
    """
    exporter = None
    resource_query = None
    pos = 0
    chunk_size = 0
    metric_keys = []
    start = 0
    end = 0
    rollup_type = ""
    rollup_minutes = 5

    def __init__(self, exporter, resource_query, chunk_size, metric_keys, start, end, rollup_type, rollup_minutes):
        """
        Creates a new Cursor

        :param exporter: The export it belongs to
        :param resource_query: The resource query to execute
        :param chunk_size: Number of resources to load at a time
        :param metric_keys: A list of keys of metrics to retrieve
        :param start: Start timestamp
        :param end: End timestamp
        :param rollup_type: Rollup type. AVG, MAX, MIN, SUM, LATEST
        :param rollup_minutes: Number of minutes to roll up
        """
        self.resource_query = resource_query
        self.exporter = exporter
        self.pos = 0
        self.chunk_size = chunk_size
        self.metric_keys = metric_keys
        self.start = start
        self.end = end
        self.rollup_type = rollup_type
        self.rollup_minutes = rollup_minutes

    def next_chunk(self):
        """
        Retrieves the next chunk, or None if no more chunks exist
        :return: The next chunk
        """
        resources = self.exporter.client.query_resources(self.resource_query, page_size=self.chunk_size, page=self.pos)
        if len(resources) == 0:
            return None
        self.pos += 1
        return self.exporter.client.query_metrics(resources, self.metric_keys, self.start, self.end, self.rollup_type, self.rollup_minutes)

    def __iter__(self):
        return self

    def __next__(self):
        chunk = self.next_chunk()
        if not chunk:
            raise StopIteration()
        return chunk



class Exporter:
    """
    Main API class.
    """
    client = None

    def __init__(self, url, username, password, auth_source = None, ignore_verify = False):
        self.client = Client(url, ignore_verify)
        self.client.login(username, password, auth_source)

    def get_resource_name(self, id):
        """
        Returns the name of a resource given its ID
        :param id: The resource ID
        :return: The resource name
        """
        return self.client.get_cached_resource_name(id)

    def export(self, resource_query, metric_keys, start, end, rollup_type = "AVG", rollup_minutes = 5):
        """
        Exports metrics for resources matching a resource query and a list of metric keys

        :param resource_query: The resource query to execute
        :param chunk_size: Number of resources to load at a time
        :param metric_keys: A list of keys of metrics to retrieve
        :param start: Start timestamp
        :param end: End timestamp
        :param rollup_type: Rollup type. AVG, MAX, MIN, SUM, LATEST
        :param rollup_minutes: Number of minutes to roll up
        :return: The full list of metrics
        """
        resources = self.client.query_resources(resource_query)
        return self.client.query_metrics(resources, metric_keys, start, end, rollup_type, rollup_minutes)

    def export_chunked(self, resource_query, metric_keys, start, end, rollup_type = "AVG", rollup_minutes = 5, chunk_size=50):
        """
        Exports metrics for resources matching a resource query and a list of metric keys divided into
        chunks of resources determined by chunk_size.

        :param resource_query: The resource query to execute
        :param chunk_size: Number of resources to load at a time
        :param metric_keys: A list of keys of metrics to retrieve
        :param start: Start timestamp
        :param end: End timestamp
        :param rollup_type: Rollup type. AVG, MAX, MIN, SUM, LATEST
        :param rollup_minutes: Number of minutes to roll up
        :param chunk_size: The number of resources to include in each chunk
        :return: The full list of metrics
        """

        return Cursor(self, resource_query, chunk_size, metric_keys, start, end, rollup_type, rollup_minutes)


