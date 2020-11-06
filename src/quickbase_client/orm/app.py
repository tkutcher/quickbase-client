import attr


@attr.s(auto_attribs=True)
class QuickBaseApp(object):
    """Class for a QuickBase app."""
    app_id: str
    realm_hostname: str
    name: str
