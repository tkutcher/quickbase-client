import pytest

from quickbase_client.orm.app import QuickBaseApp
from quickbase_client.orm.field import QB_CHECKBOX
from quickbase_client.orm.field import QB_DATE
from quickbase_client.orm.field import QB_DATETIME
from quickbase_client.orm.field import QB_NUMERIC
from quickbase_client.orm.field import QB_RICH_TEXT
from quickbase_client.orm.field import QB_TEXT
from quickbase_client.orm.field import QB_TEXT_MULTILINE
from quickbase_client.orm.field import QB_TEXT_MULTIPLE_CHOICE
from quickbase_client.orm.field import QuickBaseField
from quickbase_client.orm.report import QuickBaseReport
from quickbase_client.orm.table import QuickBaseTable


@pytest.fixture()
def example_app():
    return QuickBaseApp(app_id='abcdefg', name='QBCPY', realm_hostname='dicorp.quickbase.com')


@pytest.fixture()
def debugs_table(example_app):
    class DebugsTable(QuickBaseTable):
        __dbid__ = 'aaaaaa'
        __tablename__ = 'Debugs'
        __app__ = example_app
        __reports__ = {
            'List All': QuickBaseReport(report_id=1, name='List All')
        }

        some_basic_text_field = QuickBaseField(fid=6, field_type=QB_TEXT)
        a_multiline_text_field = QuickBaseField(fid=7, field_type=QB_TEXT_MULTILINE)
        some_checkbox = QuickBaseField(fid=8, field_type=QB_CHECKBOX)
        a_datetime = QuickBaseField(fid=9, field_type=QB_DATETIME)
        my_number = QuickBaseField(fid=10, field_type=QB_NUMERIC)
        just_a_date = QuickBaseField(fid=11, field_type=QB_DATE)
        funky_label = QuickBaseField(fid=12, field_type=QB_RICH_TEXT)
        mutlichoice = QuickBaseField(fid=13, field_type=QB_TEXT_MULTIPLE_CHOICE)
        def_ = QuickBaseField(fid=14, field_type=QB_TEXT)
        date_created = QuickBaseField(fid=1, field_type=QB_DATETIME)
        date_modified = QuickBaseField(fid=2, field_type=QB_DATETIME)
        record_id = QuickBaseField(fid=3, field_type=QB_NUMERIC)
        record_owner = QuickBaseField(fid=4, field_type=QB_NUMERIC)
        last_modified_by = QuickBaseField(fid=5, field_type=QB_NUMERIC)
    return DebugsTable
