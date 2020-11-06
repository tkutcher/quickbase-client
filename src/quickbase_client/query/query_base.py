
class QuickBaseQuery(object):
    """A base object for all of the data for a query.

    :ivar where: The where string, e.g. ``"{7.EX.'18'}"``
    """

    def __init__(self, where, options=None, group_by=None, sort_by=None, select=None):
        self.where = where
        self.options = options
        self.group_by = group_by
        self.sort_by = sort_by
        self.select = select
