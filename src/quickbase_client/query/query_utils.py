from datetime import date
from datetime import datetime

from quickbase_client.orm.field import QuickBaseField


DATE_FMT = '%m-%d-%Y'
DATETIME_FMT = '%m-%d-%Y %l:%M%p'


def query_value_stringify(val, _quote=True):
    def quoter(v):
        return f"'{v}'" if _quote else v

    if isinstance(val, datetime):
        return quoter(val.strftime(DATETIME_FMT))
    if isinstance(val, date):
        return quoter(val.strftime(DATE_FMT))
    if isinstance(val, bool):
        return quoter('true' if val else 'false')
    if isinstance(val, list):
        return quoter('; '.join([query_value_stringify(v, _quote=False) for v in val]))
    if isinstance(val, QuickBaseField):
        return quoter(f'_FID_{val.fid}')
    if isinstance(val, int) or isinstance(val, float):
        return str(val)  # don't quote
    return quoter(str(val))


def make_query_string(field, operator, matching_value):
    fid = field.fid if isinstance(field, QuickBaseField) else field
    val = query_value_stringify(matching_value)
    return f"{{'{fid}'.{operator}.{val}}}"
