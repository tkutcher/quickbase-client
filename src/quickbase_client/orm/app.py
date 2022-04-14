import attr


@attr.s(auto_attribs=True)
class QuickbaseApp(object):
    """Class for a QuickBase app."""

    app_id: str
    realm_hostname: str
    name: str


QuickBaseApp = QuickbaseApp  # alias - TODO - delete in future
