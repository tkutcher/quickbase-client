import attr


@attr.s(auto_attribs=True)
class QuickBaseReport(object):
    report_id: str
    name: str
    type: str
    description: str
