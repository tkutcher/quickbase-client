import json
from datetime import date
from datetime import datetime

import pytest

from quickbase_client.orm.app import QuickbaseApp
from quickbase_client.orm.field import QB_CHECKBOX
from quickbase_client.orm.field import QB_DATE
from quickbase_client.orm.field import QB_DATETIME
from quickbase_client.orm.field import QB_RICH_TEXT
from quickbase_client.orm.field import QB_TEXT
from quickbase_client.orm.field import QB_TEXT_MULTILINE
from quickbase_client.orm.field import QB_TEXT_MULTIPLE_CHOICE
from quickbase_client.orm.field import QB_TEXT_MULTI_SELECT
from quickbase_client.orm.field import QuickbaseField
from quickbase_client.orm.serialize import QuickbaseJsonEncoder
from quickbase_client.orm.serialize import RecordJsonSerializer
from quickbase_client.orm.table import QuickbaseTable


@pytest.fixture()
def example_table():
    class ExampleTable(QuickbaseTable):
        __dbid__ = "bqx7xre7a"
        __tablename__ = "Examples"
        __app__ = QuickbaseApp(
            app_id="abcdefg", name="QBCPY", realm_hostname="example.quickbase.com"
        )
        text_field = QuickbaseField(fid=8, field_type=QB_TEXT)
        date_field = QuickbaseField(fid=6, field_type=QB_DATETIME)
        bool_field = QuickbaseField(fid=7, field_type=QB_CHECKBOX)
        date_time_as_date = QuickbaseField(fid=900, field_type=QB_DATE)
        date_time_as_date_time = QuickbaseField(fid=901, field_type=QB_DATETIME)
        rich_text_as_rich_text = QuickbaseField(fid=902, field_type=QB_RICH_TEXT)
        text_as_ascii_text = QuickbaseField(fid=903, field_type=QB_TEXT)
        text_multiline_as_ascii_text = QuickbaseField(
            fid=904, field_type=QB_TEXT_MULTILINE
        )
        text_multi_select_as_ascii_text = QuickbaseField(
            fid=905, field_type=QB_TEXT_MULTI_SELECT
        )
        text_multiple_choice_as_ascii_text = QuickbaseField(
            fid=906, field_type=QB_TEXT_MULTIPLE_CHOICE
        )

    return ExampleTable


class TestRecordJsonSerializer:
    def test_serialize_makes_dict_by_fid(self, example_table):
        rec = example_table(
            text_field="hello",
            date_field=date(year=2020, month=10, day=28),
            bool_field=True,
        )
        serializer = RecordJsonSerializer(example_table)
        data = serializer.serialize(rec)
        assert all(x in data for x in range(6, 8))

    def test_serialize_adds_value_level(self, example_table):
        rec = example_table(
            text_field="hello",
            date_field=date(year=2020, month=10, day=28),
            bool_field=True,
        )
        serializer = RecordJsonSerializer(example_table)
        data = serializer.serialize(rec)
        assert all("value" in data[x + 1] for x in range(6, 8))

    def test_serialize_datetime_as_date(self, example_table):
        # arrange
        dt = datetime.now()
        rec = example_table(date_time_as_date=dt)
        serializer = RecordJsonSerializer(example_table)
        # act
        data = serializer.serialize(rec)
        # assert
        assert data[example_table.schema.date_time_as_date.fid]["value"] == dt.date()

    def test_serialize_datetime_as_datetime(self, example_table):
        # arrange
        dt = datetime.now()
        rec = example_table(date_time_as_date_time=dt)
        serializer = RecordJsonSerializer(example_table)
        # act
        data = serializer.serialize(rec)
        # assert
        assert data[example_table.schema.date_time_as_date_time.fid]["value"] == dt

    def test_serialize_rich_text_as_rich_text(self, example_table):
        # arrange
        s = "<p>Tobias Fünke has been to <b>Juárez</b>, \nMéxico with his niña &amp; hermosa.</p>"
        rec = example_table(rich_text_as_rich_text=s)
        serializer = RecordJsonSerializer(example_table)
        # act
        data = serializer.serialize(rec)
        # assert
        assert (
            data[example_table.schema.rich_text_as_rich_text.fid]["value"] == s
        ), "Rich Text should be left untouched"

    def test_serialize_accented_text_as_accented_text_with_option(self, example_table):
        # arrange
        s = "Tobias Fünke has been to Juárez, México with his niña"
        rec = example_table(text_field=s)
        serializer = RecordJsonSerializer(example_table, normalize_unicode=False)
        # act
        data = serializer.serialize(rec)
        # assert
        assert data[example_table.schema.text_field.fid]["value"] == s

    def test_serialize_ignores_non_strings(self, example_table):
        # arrange
        non_string = 42
        rec = example_table(text_field=non_string)
        serializer = RecordJsonSerializer(example_table)
        # act
        data = serializer.serialize(rec)
        # assert
        assert data[example_table.schema.text_field.fid]["value"] == non_string

    @pytest.mark.parametrize(
        "attr_name",
        [
            ("text_as_ascii_text"),
            ("text_multiline_as_ascii_text"),
            ("text_multi_select_as_ascii_text"),
            ("text_multiple_choice_as_ascii_text"),
        ],
    )
    def test_serialize_accented_text_as_ascii_text(self, attr_name, example_table):
        # arrange
        s = "Tobias Fünke has been to Juárez, México with his niña"
        rec = example_table(**{attr_name: s})
        fid = example_table.get_field_info(attr_name).fid
        serializer = RecordJsonSerializer(example_table)
        expect = "Tobias Funke has been to Juarez, Mexico with his nina"
        # act
        data = serializer.serialize(rec)
        # assert
        assert data[fid]["value"] == expect

    def test_deserialize_to_debugs_table(self, debugs_table, mock_json_loader):
        data = mock_json_loader("get_records_for_table_aaaaaa.json")
        serializer = RecordJsonSerializer(table_cls=debugs_table)
        o = serializer.deserialize(data["data"][0])
        assert o.some_basic_text_field == "First field"
        assert o.my_number == 18
        assert o.just_a_date == date(year=2020, month=10, day=3)


class TestJsonEncoder:
    def test_encodes_dates(self):
        data = {1: date(year=2020, month=12, day=9), 2: True, 3: "hello"}
        s = json.dumps(data, cls=QuickbaseJsonEncoder)
        assert "2020-12-09" in s
        assert "true" in s
        assert "hello" in s

    def test_encodes_datetimes(self):
        data = {1: datetime(year=2020, month=12, day=9, hour=2), 2: True, 3: "hello"}
        s = json.dumps(data, cls=QuickbaseJsonEncoder)
        assert "2020-12-09T02:00:00" in s
        assert "." not in json.loads(s)["1"]
