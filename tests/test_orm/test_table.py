import pytest

from quickbase_client.client.table_client import QuickBaseTableClient
from quickbase_client.orm.app import QuickBaseApp
from quickbase_client.orm.field import QB_NUMERIC
from quickbase_client.orm.field import QB_TEXT
from quickbase_client.orm.field import QuickBaseField
from quickbase_client.orm.report import QuickBaseReport
from quickbase_client.orm.table import QuickBaseTable


@pytest.fixture()
def example_table():
    class ExampleTable(QuickBaseTable):
        __dbid__ = 'bqx7xre7a'
        __tablename__ = 'Examples'
        __app__ = QuickBaseApp(app_id='abcdefg', name='QBCPY', realm_hostname='example.quickbase.com')
        __reports__ = {
            'Report A': QuickBaseReport(report_id=1, name='Report A')
        }
        field_1 = QuickBaseField(fid=6, field_type=QB_TEXT)
        field_2 = QuickBaseField(fid=7, field_type=QB_NUMERIC)
    return ExampleTable


class TestQuickBaseTable:

    def test_can_create_record_objects(self, example_table):
        rec = example_table(field_1='A', field_2=46)
        assert rec.field_1 == 'A'
        assert rec.field_2 == 46

    def test_not_all_required(self, example_table):
        rec = example_table(field_1='A')
        assert rec.field_1 == 'A'
        assert rec.field_2 is None

    def test_cannot_set_unspecified_attributes(self, example_table):
        with pytest.raises(AttributeError) as e:
            _ = example_table(this_does_not_exist='hello')
            assert 'this_does_not_exist' in str(e)

    def test_get_field_info(self, example_table):
        field_info = example_table.get_field_info('field_1')
        assert field_info.field_type == QB_TEXT

    def test_app_id(self, example_table):
        assert example_table.app_id() == 'abcdefg'

    def test_schema(self, example_table):
        assert example_table.schema.field_1 == example_table.get_field_info('field_1')

    def test_get_report(self, example_table):
        assert example_table.get_report('Report A').report_id == 1

    def test_make_client(self, example_table):
        c = example_table.client('foo')
        assert isinstance(c, QuickBaseTableClient)
