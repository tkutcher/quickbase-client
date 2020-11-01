import json
from datetime import date

import pytest
from quickbase_client.orm.app import QuickBaseApp
from quickbase_client.orm.field import QuickBaseField
from quickbase_client.orm.field import QuickBaseFieldType as Qb
from quickbase_client.orm.serialize import QuickBaseJsonEncoder
from quickbase_client.orm.serialize import RecordJsonSerializer
from quickbase_client.orm.table import QuickBaseTable


@pytest.fixture()
def example_table():
    class ExampleTable(QuickBaseTable):
        __dbid__ = 'bqx7xre7a'
        __tablename__ = 'Examples'
        __app__ = QuickBaseApp(app_id='abcdefg', name='QBCPY', realm_hostname='example.quickbase.com')
        text_field = QuickBaseField(fid=8, field_type=Qb.TEXT)
        date_field = QuickBaseField(fid=6, field_type=Qb.DATETIME)
        bool_field = QuickBaseField(fid=7, field_type=Qb.CHECKBOX)
    return ExampleTable


class TestRecordJsonSerializer:

    def test_serialize_makes_dict_by_fid(self, example_table):
        rec = example_table(
            text_field='hello',
            date_field=date(year=2020, month=10, day=28),
            bool_field=True)
        serializer = RecordJsonSerializer()
        data = serializer.serialize(rec)
        assert all(x in data for x in range(6, 8))

    def test_serialize_adds_value_level(self, example_table):
        rec = example_table(
            text_field='hello',
            date_field=date(year=2020, month=10, day=28),
            bool_field=True)
        serializer = RecordJsonSerializer()
        data = serializer.serialize(rec)
        assert all('value' in data[x + 1] for x in range(6, 8))


class TestJsonEncoder:

    def test_encodes_dates(self):
        data = {1: date(year=2020, month=12, day=9)}
        s = json.dumps(data, cls=QuickBaseJsonEncoder)
        assert '2020-12-09' in s
