class ResponsePager:
    """Object to pass to methods (query) to manage pagination.

    When calling something like QuickbaseTableClient.query, you can pass a ResponsePager,
    and repeatedly make requests while :meth:`~more_remaining` is True.

    .. code:: python

       pager = ResponsePager()
       while pager.more_remaining():
           recs = my_client.query(pager=pager)

    """

    def __init__(self):
        self.num_calls = 0
        self.next_skip = 0
        self.total_records = -1

    def update_from_metadata(self, metadata):
        self.num_calls += 1
        self.total_records = metadata["totalRecords"]
        self.next_skip = metadata["skip"] + metadata["numRecords"]

    def get_options(self):
        return {"skip": self.next_skip}

    def more_remaining(self) -> bool:
        """Returns true if there is another request to be made."""
        return self.total_records == -1 or self.next_skip < self.total_records
