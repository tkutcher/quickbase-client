class QuickbaseQuery(object):
    """A base object for all of the data for a query.

    .. note::
        Current alias of ``QuickbaseQuery`` for backwards compatibility.

    :ivar str where: The where string, e.g. ``"{7.EX.'18'}"``
    :ivar dict options: Additional options to pass to the Quickbase runQuery endpoint
    :ivar list[dict] group_by: The groupBy for the Quickbase runQuery endpoint
    :ivar list[int] select: The list of field ID's to return
    """

    def __init__(self, where, options=None, group_by=None, sort_by=None, select=None):
        self.where = where
        self.options = options
        self.group_by = group_by
        self.sort_by = sort_by
        self.select = select


QuickBaseQuery = QuickbaseQuery
