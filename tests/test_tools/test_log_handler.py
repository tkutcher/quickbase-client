import logging

import pytest

from quickbase_client import QuickbaseApp
from quickbase_client import QuickbaseField
from quickbase_client import QuickbaseFieldType as Qb
from quickbase_client import QuickbaseTable
from quickbase_client.tools.log_handler import QuickbaseLogHandler

_MyApp = QuickbaseApp(
    app_id="blah", name="bleh", realm_hostname="builderprogram-tkutcher.quickbase.com"
)


class _MyLogsTable(QuickbaseTable):
    __dbid__ = "log"
    __app__ = _MyApp
    level = QuickbaseField(fid=6, field_type=Qb.TEXT)
    message = QuickbaseField(fid=7, field_type=Qb.TEXT)
    when = QuickbaseField(fid=8, field_type=Qb.DATETIME)


class _NotALogTable(QuickbaseTable):
    __dbid__ = "log"
    __app__ = _MyApp
    level = QuickbaseField(fid=6, field_type=Qb.TEXT)


MOCK_LOG_LEVEL = 10
MOCK_LOG_MSG = "mock!"
MOCK_LOG: logging.LogRecord = logging.LogRecord(
    name="mock",
    level=MOCK_LOG_LEVEL,
    pathname="mock",
    lineno=1,
    msg=MOCK_LOG_MSG,
    args=None,
    exc_info=None,
)


class TestLogHandler:
    def test_requires_correct_properties_if_default_record_factory(self):
        with pytest.raises(TypeError):
            client = _NotALogTable.client("foo")
            QuickbaseLogHandler(client)

    def test_posts_log_record(self, mocker):
        client = _MyLogsTable.client("foo")
        handler = QuickbaseLogHandler(client)
        spy = mocker.spy(client.api._rf.session, "request")
        handler._do_emit(MOCK_LOG)
        _, k = spy.call_args
        fid = str(_MyLogsTable.schema.level.fid)
        assert k["json"]["data"][0][fid]["value"] == MOCK_LOG_LEVEL

    def test_create_with_record_factory(self, mocker):
        client = _MyLogsTable.client("foo")
        spy = mocker.spy(client.api._rf.session, "request")

        def _mock_rf(record):
            return _MyLogsTable(message=record.msg)

        handler = QuickbaseLogHandler.with_record_factory(client, _mock_rf)
        handler._do_emit(MOCK_LOG)
        _, k = spy.call_args
        assert str(_MyLogsTable.schema.level.fid) not in k["json"]["data"][0]
        assert str(_MyLogsTable.schema.message.fid) in k["json"]["data"][0]
