from quickbase_client.query.query_base import QuickBaseQuery
from quickbase_client.query.query_utils import make_query_string


def qb_query_ast(func):
    def _wrap(*args, **kwargs):
        return QuickBaseQuery(where=func(*args, **kwargs))
    return _wrap


def _conjunction(kind, *clauses):
    return f'({kind.join([c.where for c in clauses])})'


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
    return make_query_string(field, 'HAS', val)


@qb_query_ast
def not_has_(field, val):
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
