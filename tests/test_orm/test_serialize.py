import json
from datetime import date

from quickbase_client.orm.serialize import QuickBaseJsonEncoder
from quickbase_client.orm.serialize import RecordJsonSerializer


class TestRecordJsonSerializer:

    def test_encode_simple(self, example_table):
        rec = example_table(
            field_1='A',
            field_2=['A', 'B'],
            field_3=99.2,
            field_4=date(year=2020, month=10, day=28))
        serializer = RecordJsonSerializer()
        data = serializer.serialize(rec)
        assert all((x + 1) in data for x in range(3))


class TestJsonEncoder:

    def test_encodes_dates(self):
        data = {1: date(year=2020, month=12, day=9)}
        s = json.dumps(data, cls=QuickBaseJsonEncoder)
        assert '2020-12-09' in s
