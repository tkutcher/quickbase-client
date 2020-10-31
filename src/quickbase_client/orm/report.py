import attr


@attr.s(auto_attribs=True)
class QuickBaseReport(object):
    report_id: int
    name: str
    type: str = ''
    description: str = ''
