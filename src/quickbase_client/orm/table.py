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
        mappings = dict()
        mcs._schema = QuickBaseTableSchema()

        for k, v in attrs.items():
            if isinstance(v, QuickBaseField):
                mappings[k] = v
                setattr(mcs._schema, k, v)

        # Delete these properties that are already stored in the dictionary
        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings  # Save mapping between attributes and columns
        attrs['__schema__'] = mcs._schema  # Save mapping between attributes and columns
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
        self._schema = QuickBaseTableSchema()

        for attr, field_def in self.__mappings__.items():
            setattr(self, attr, None)
            setattr(self._schema, attr, field_def)

        for name, value in kwargs.items():
            if name not in self.__mappings__:
                raise AttributeError(f'no attribute named {name}')
            setattr(self, name, value)

    # QUESTION - does this psuedo-typehint help IDE's?
    # @classmethod
    # def schema(cls) -> 'QuickBaseTable':
    #     return cls.__schema__

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
