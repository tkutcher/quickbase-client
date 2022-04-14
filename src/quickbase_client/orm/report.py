import attr


@attr.s(auto_attribs=True)
class QuickbaseReport(object):
    report_id: int
    name: str
    type: str = ""
    description: str = ""


QuickBaseReport = QuickbaseReport  # alias - TODO - delete in future
