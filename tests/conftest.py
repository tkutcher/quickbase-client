import json
import pathlib

import pytest

from quickbase_client.orm.app import QuickbaseApp
from quickbase_client.orm.field import QB_CHECKBOX
from quickbase_client.orm.field import QB_DATE
from quickbase_client.orm.field import QB_DATETIME
from quickbase_client.orm.field import QB_NUMERIC
from quickbase_client.orm.field import QB_RICH_TEXT
from quickbase_client.orm.field import QB_TEXT
from quickbase_client.orm.field import QB_TEXT_MULTILINE
from quickbase_client.orm.field import QB_TEXT_MULTIPLE_CHOICE
from quickbase_client.orm.field import QuickbaseField
from quickbase_client.orm.report import QuickbaseReport
from quickbase_client.orm.table import QuickbaseTable
import requests_mock as requests_mock_


@pytest.fixture()
def example_app():
    return QuickbaseApp(
        app_id="abcdefg", name="QBCPY", realm_hostname="dicorp.quickbase.com"
    )


@pytest.fixture()
def debugs_table(example_app):
    class DebugsTable(QuickbaseTable):
        __dbid__ = "aaaaaa"
        __tablename__ = "Debugs"
        __app__ = example_app
        __reports__ = {"List All": QuickbaseReport(report_id=1, name="List All")}

        some_basic_text_field = QuickbaseField(fid=6, field_type=QB_TEXT)
        a_multiline_text_field = QuickbaseField(fid=7, field_type=QB_TEXT_MULTILINE)
        some_checkbox = QuickbaseField(fid=8, field_type=QB_CHECKBOX)
        a_datetime = QuickbaseField(fid=9, field_type=QB_DATETIME)
        my_number = QuickbaseField(fid=10, field_type=QB_NUMERIC)
        just_a_date = QuickbaseField(fid=11, field_type=QB_DATE)
        funky_label = QuickbaseField(fid=12, field_type=QB_RICH_TEXT)
        mutlichoice = QuickbaseField(fid=13, field_type=QB_TEXT_MULTIPLE_CHOICE)
        def_ = QuickbaseField(fid=14, field_type=QB_TEXT)
        date_created = QuickbaseField(fid=1, field_type=QB_DATETIME)
        date_modified = QuickbaseField(fid=2, field_type=QB_DATETIME)
        record_id = QuickbaseField(fid=3, field_type=QB_NUMERIC)
        record_owner = QuickbaseField(fid=4, field_type=QB_NUMERIC)
        last_modified_by = QuickbaseField(fid=5, field_type=QB_NUMERIC)

    return DebugsTable


def _data_from_file(data_file):
    p = pathlib.Path(__file__).parent / "data" / "mocks" / data_file
    with open(str(p), "r") as f:
        return json.load(f)


_mocks = [
    ("GET", "/apps/abcdef", "get_app_abcdef.json"),
    ("GET", "/tables?appId=abcdef", "get_tables_for_app_abcdef.json"),
    ("GET", "/fields?tableId=aaaaaa", "get_fields_for_table_aaaaaa.json"),
    ("GET", "/fields?tableId=bbbbbb", "get_fields_for_table_bbbbbb.json"),
    ("GET", "/fields?tableId=cccccc", "get_fields_for_table_cccccc.json"),
    ("POST", "/records/query", "get_records_for_table_aaaaaa.json"),
]


@pytest.fixture()
def qb_api_mock(requests_mock):
    for method, endpoint, f in _mocks:
        requests_mock.request(
            method, f"https://api.quickbase.com/v1{endpoint}", json=_data_from_file(f)
        )


@pytest.fixture(autouse=True)
def _no_real_requests(requests_mock):
    """Make sure no real HTTP requests are sent."""
    requests_mock.request(requests_mock_.ANY, requests_mock_.ANY, json={})


@pytest.fixture()
def mock_json_loader():
    return _data_from_file
