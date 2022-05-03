"""
The table module includes a class :class:`~QuickbaseTable` that facilitates an ORM
to QuickBase API JSON through a meta class also defined in this module.
"""

from typing import Dict

from quickbase_client.orm.app import QuickbaseApp
from quickbase_client.orm.field import QuickbaseField
from quickbase_client.orm.report import QuickbaseReport


# help from
# https://programmer.help/blogs/python-how-to-implement-orm-with-metaclasses.html


class QuickbaseTableMeta(type):
    """Meta-class which builds a dunder to store field data.

    Stores a mapping of attribute name --> QuickbaseFieldType in ``__mappings__``,

    """

    def __new__(mcs, name, bases, attrs):
        mappings = {}
        fidmap = {}
        _schema = QuickbaseTableSchema()

        for k, v in attrs.items():
            if isinstance(v, QuickbaseField):
                mappings[k] = v
                fidmap[v.fid] = k
                setattr(_schema, k, v)

        # Delete these properties that are already stored in the dictionary
        for k in mappings.keys():
            attrs.pop(k)

        attrs["__mappings__"] = mappings
        attrs["__fidmap__"] = fidmap
        attrs["__schema__"] = _schema
        return type.__new__(mcs, name, bases, attrs)

    @property
    def schema(cls):
        return cls.__schema__  # noqa


class QuickbaseTableSchema(object):
    """Used to get :class:`~QuickbaseField` data and not the value of the field."""

    pass


class QuickbaseTable(metaclass=QuickbaseTableMeta):
    """
    Base class for a table object.

    :ivar __dbid__: The string table ID (the part after /db in the URL).
    :ivar __tablename__: The english name of the table.
    :ivar __app__: The :class:`~QuickbaseApp` the table belongs to.
    :ivar __reports__: Lookup of :class:`~QuickbaseReport` objects for this table.
    :cvar schema: The object to reference field types (rather than field data).
    """

    __dbid__ = None
    __tablename__ = ""
    __app__: QuickbaseApp = None

    __reports__: Dict[str, QuickbaseReport] = {}

    def __init__(self, **kwargs):

        for attr, field_def in self.__mappings__.items():  # noqa
            v = kwargs.pop(attr) if attr in kwargs else None
            setattr(self, attr, v)

        for name, _ in kwargs.items():  # simple way to get the kwarg name if not empty
            raise AttributeError(f"no attribute named {name}")

    @classmethod
    def app_id(cls) -> str:
        """Alias to the app's ID."""
        return cls.__app__.app_id

    @classmethod
    def realm_hostname(cls) -> str:
        """Alias to the app's realm hostname."""
        return cls.__app__.realm_hostname

    @classmethod
    def get_field_info(cls, attr: str) -> QuickbaseField:
        """Get the field info for a given attribute rather than the data.

        :param attr: String name of the attribute.
        """
        return cls.__mappings__[attr]  # noqa

    @classmethod
    def get_report(cls, name: str):
        """Get a report by it's name.

        :param name: The name of the report
        """
        return cls.__reports__[name]

    @classmethod
    def get_attr_from_fid(cls, fid: int):
        """Lookup an attribute name by it's field ID.

        :param fid: The field ID.
        """
        return cls.__fidmap__[fid]  # noqa

    @classmethod
    def client(cls, user_token: str, **kwargs):
        """Factory method to create a :class:`~QuickbaseTableClient` for this table.

        :param user_token: The user token for authentication.
        :param kwargs: Forwarded to :class:`~QuickbaseTableClient`.
        """
        from quickbase_client.client.table_client import QuickbaseTableClient

        return QuickbaseTableClient(cls, user_token, **kwargs)


QuickBaseTable = QuickbaseTable  # alias - TODO - delete in future.
