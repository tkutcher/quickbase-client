import pytest
from quickbase_client.orm.app import QuickBaseApp
from quickbase_client.orm.field import QuickBaseField
from quickbase_client.orm.field import QuickBaseFieldType as Qb
from quickbase_client.orm.table import QuickBaseTable


@pytest.fixture()
def example_app():
    return QuickBaseApp(app_id='aaaaaa', name='Example', realm_hostname='example.quickbase.com')


@pytest.fixture()
def example_table(example_app):
    class ExampleTable(QuickBaseTable):
        __dbid__ = 'abc123'
        name = 'Example'
        app = example_app
        field_1 = QuickBaseField(fid=1, field_type=Qb.TEXT)
        field_2 = QuickBaseField(fid=2, field_type=Qb.TEXT_MULTI_SELECT)
        field_3 = QuickBaseField(fid=3, field_type=Qb.NUMERIC_CURRENCY)
        field_4 = QuickBaseField(fid=4, field_type=Qb.DATE)
    return ExampleTable

