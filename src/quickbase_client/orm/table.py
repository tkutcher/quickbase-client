from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from quickbase_client.orm.field import QuickBaseField

# help from https://programmer.help/blogs/python-how-to-implement-orm-with-metaclasses.html


class QuickBaseTableMeta(type):
    """ Meta-class which builds a dunder to store the mappings of attribute
        name --> QuickBaseFieldType
    """
    def __new__(mcs, name, bases, attrs):
        mappings = dict()

        for k, v in attrs.items():
            if isinstance(v, QuickBaseField):
                mappings[k] = v

        # Delete these properties that are already stored in the dictionary
        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings  # Save mapping between attributes and columns
        return type.__new__(mcs, name, bases, attrs)


class QuickBaseTable(metaclass=QuickBaseTableMeta):
    __dbid__ = None

    def __init__(self, **kwargs):
        for attr in self.__mappings__:
            setattr(self, attr, None)
        for name, value in kwargs.items():
            if name not in self.__mappings__:
                raise AttributeError(f'no attribute named {name}')
            setattr(self, name, value)

    @classmethod
    def get_field_info(cls, attr: str) -> QuickBaseField:
        return cls.__mappings__[attr]

    def as_field_pairs(self) -> List[Tuple[QuickBaseField, Any]]:
        return [(self.get_field_info(attr), v) for attr, v in self.__dict__.items()]
