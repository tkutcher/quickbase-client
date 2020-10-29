import attr


@attr.s(auto_attribs=True)
class QuickBaseApp(object):
    app_id: str
    realm_hostname: str
    name: str
