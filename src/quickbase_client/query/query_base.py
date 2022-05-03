class QuickbaseQuery(object):
    """A base object for all of the data for a query.

    .. note::
        Current alias of ``QuickbaseQuery`` for backwards compatibility.

    :param Optional[str] where: The where string, e.g. ``"{7.EX.'18'}"``

    :param dict options:
        Additional options to pass to the Quickbase runQuery endpoint.

    :param list[dict] group_by:
        The groupBy for the Quickbase runQuery endpoint.

    :param list[dict] sort_by:
        The sortBy for the Quickbase runQuery endpoint.

    :param list[int] select:
        The list of field ID's to return. Note that Quickbase by default (i.e. if
        this parameter is left as ``None``) only returns the "default" fields for
        the table.
    """

    def __init__(self, where, options=None, group_by=None, sort_by=None, select=None):
        self.where = where
        self.options = options
        self.group_by = group_by
        self.sort_by = sort_by
        self.select = select


QuickBaseQuery = QuickbaseQuery
