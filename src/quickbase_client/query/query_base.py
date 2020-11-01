
class QuickBaseQuery(object):

    def __init__(self, where, options=None, group_by=None, sort_by=None, select=None):
        self.where = where
        self.options = options
        self.group_by = group_by
        self.sort_by = sort_by
        self.select = select
