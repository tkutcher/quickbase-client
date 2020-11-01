import datetime

import pytest
from quickbase_client.orm.field import QuickBaseField
from quickbase_client.orm.field import QuickBaseFieldType as Qb
from quickbase_client.query.query_utils import make_query_string
from quickbase_client.query.query_utils import query_value_stringify


@pytest.mark.parametrize('val,expect', [
    ('hello', "'hello'"),
    (datetime.datetime(year=2020, month=10, day=31), "'10-31-2020 12:00AM'"),
    (datetime.date(year=2020, month=10, day=31), "'10-31-2020'"),
    (True, "'true'"),
    (False, "'false'"),
    (QuickBaseField(fid=18, field_type=Qb.TEXT), "'_FID_18'"),
    (['val1', 'val2'], "'val1; val2'"),
    (18, '18')
])
def test_query_value_stringify(val, expect):
    assert query_value_stringify(val) == expect


class TestMakeQueryString:

    mock_field = QuickBaseField(fid=18, field_type=Qb.TEXT)

    def test_simple(self):
        s = make_query_string('18', 'EX', 19)
        assert s == "{'18'.EX.19}"

    def test_pass_field_obj(self):
        s = make_query_string(self.mock_field, 'EX', 19)
        assert s == "{'18'.EX.19}"
