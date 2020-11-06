"""This module includes functions which create :class:`~QuickBaseQuery` objects.

These can be assembled in an AST-like fashion to build a complex query using higher-level
english-readable functions rather than going through the query language (note you can always
create a :class:`~QuickBaseQuery` and provide the where string to use that).

Example:

.. code-block:: python

    schema = MyTable.schema
    my_query = and_(
        eq_(schema.date_opened, schema.date_created),
        on_or_before_(schema.date_closed, date(2020, 11, 16))
    )
    print(my_query.where) # ({'9'.EX.'_FID_1'}AND{'10'.OBF.'11-16-2020'})

All of the methods (except the two conjunction ones), take a
:class:`~QuickBaseField` and a value as a parameter. If you pass a `QuickBaseField`
for the value, it will compare to the actual field (see above). But note if you pass
an attribute of a QuickBaseTable class it would be the value in memory of that attribute.
If you want to compare to the actual field, use the schema property of the table or
:meth:`quickbase_client.QuickBaseTable.get_field_info`.


Note all of these methods are named with a trailing ``_`` to maintain consistency and
never clash with a python keyword or anything.
"""


from quickbase_client.query.query_base import QuickBaseQuery
from quickbase_client.query.query_utils import make_query_string


def qb_query_ast(func):
    def _wrap(*args, **kwargs):
        return QuickBaseQuery(where=func(*args, **kwargs))
    return _wrap


def _conjunction(kind, *clauses):
    return f'({kind.join([c.where for c in clauses])})'


# Note the decorator makes it tricky for sphinx to read the autodoc so docs
# are just in the docs folder for these functions.

@qb_query_ast
def or_(*clauses):
    return _conjunction('OR', *clauses)


@qb_query_ast
def and_(*clauses):
    return _conjunction('AND', *clauses)


@qb_query_ast
def contains_(field, val):
    return make_query_string(field, 'CT', val)


@qb_query_ast
def not_contains_(field, val):
    return make_query_string(field, 'XCT', val)


@qb_query_ast
def has_(field, val):
    """Has (HAS)."""
    return make_query_string(field, 'HAS', val)


@qb_query_ast
def not_has_(field, val):
    """Not Has (XHAS)."""
    return make_query_string(field, 'XHAS', val)


@qb_query_ast
def eq_(field, val):
    return make_query_string(field, 'EX', val)


# QUESTION - don't understand this operator in their query language...
@qb_query_ast
def true_(field, val):
    return make_query_string(field, 'TV', val)


@qb_query_ast
def not_eq_(field, val):
    return make_query_string(field, 'XEX', val)


@qb_query_ast
def starts_with_(field, val):
    return make_query_string(field, 'SW', val)


@qb_query_ast
def not_starts_width_(field, val):
    return make_query_string(field, 'XSW', val)


@qb_query_ast
def before_(field, val):
    return make_query_string(field, 'BF', val)


@qb_query_ast
def on_or_before_(field, val):
    return make_query_string(field, 'OBF', val)


@qb_query_ast
def after_(field, val):
    return make_query_string(field, 'AF', val)


@qb_query_ast
def on_or_after_(field, val):
    return make_query_string(field, 'OAF', val)


@qb_query_ast
def during_(field, val):
    return make_query_string(field, 'IR', val)


@qb_query_ast
def not_during_(field, val):
    return make_query_string(field, 'XIR', val)


@qb_query_ast
def lt_(field, val):
    return make_query_string(field, 'LT', val)


@qb_query_ast
def lte_(field, val):
    return make_query_string(field, 'LTE', val)


@qb_query_ast
def gt_(field, val):
    return make_query_string(field, 'GT', val)


@qb_query_ast
def gte_(field, val):
    return make_query_string(field, 'GTE', val)
