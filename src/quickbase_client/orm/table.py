from typing import Dict

from quickbase_client.orm.app import QuickBaseApp
from quickbase_client.orm.field import QuickBaseField
from quickbase_client.orm.report import QuickBaseReport


# help from https://programmer.help/blogs/python-how-to-implement-orm-with-metaclasses.html


class QuickBaseTableMeta(type):
    """ Meta-class which builds a dunder to store the mappings of attribute
        name --> QuickBaseFieldType
    """
    def __new__(mcs, name, bases, attrs):
        mappings = {}
        fidmap = {}
        mcs._schema = QuickBaseTableSchema()

        for k, v in attrs.items():
            if isinstance(v, QuickBaseField):
                mappings[k] = v
                fidmap[v.fid] = k
                setattr(mcs._schema, k, v)

        # Delete these properties that are already stored in the dictionary
        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings
        attrs['__fidmap__'] = fidmap
        attrs['__schema__'] = mcs._schema
        return type.__new__(mcs, name, bases, attrs)

    @property
    def schema(cls):
        return cls._schema


class QuickBaseTableSchema(object):
    pass


class QuickBaseTable(metaclass=QuickBaseTableMeta):
    __dbid__ = None
    __tablename__ = ''
    __app__: QuickBaseApp = None

    __reports__: Dict[str, QuickBaseReport] = {}

    def __init__(self, **kwargs):

        for attr, field_def in self.__mappings__.items():
            v = kwargs.pop(attr) if attr in kwargs else None
            setattr(self, attr, v)

        for name, _ in kwargs.items():  # simple way to get the kwarg name if not empty
            raise AttributeError(f'no attribute named {name}')

    @classmethod
    def app_id(cls) -> str:
        return cls.__app__.app_id

    @classmethod
    def realm_hostname(cls) -> str:
        return cls.__app__.realm_hostname

    @classmethod
    def get_field_info(cls, attr: str) -> QuickBaseField:
        return cls.__mappings__[attr]

    @classmethod
    def get_report(cls, name):
        return cls.__reports__[name]

    @classmethod
    def get_attr_from_fid(cls, fid):
        return cls.__fidmap__[fid]

    @classmethod
    def client(cls, user_token):
        from quickbase_client.client.table_client import QuickBaseTableClient
        return QuickBaseTableClient(cls, user_token)
