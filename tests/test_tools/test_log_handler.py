import logging

import pytest

from quickbase_client import QuickBaseApp
from quickbase_client import QuickBaseField
from quickbase_client import QuickBaseFieldType as Qb
from quickbase_client import QuickBaseTable
from quickbase_client.tools.log_handler import QuickbaseLogHandler


_MyApp = QuickBaseApp(
    app_id='blah',
    name='bleh',
    realm_hostname='builderprogram-tkutcher.quickbase.com'
)


class _MyLogsTable(QuickBaseTable):
    __dbid__ = 'log'
    __app__ = _MyApp
    level = QuickBaseField(fid=6, field_type=Qb.TEXT)
    message = QuickBaseField(fid=7, field_type=Qb.TEXT)
    when = QuickBaseField(fid=8, field_type=Qb.DATETIME)


class _NotALogTable(QuickBaseTable):
    __dbid__ = 'log'
    __app__ = _MyApp
    level = QuickBaseField(fid=6, field_type=Qb.TEXT)


MOCK_LOG_LEVEL = 10
MOCK_LOG_MSG = 'mock!'
MOCK_LOG: logging.LogRecord = logging.LogRecord(
    name='mock',
    level=MOCK_LOG_LEVEL,
    pathname='mock',
    lineno=1,
    msg=MOCK_LOG_MSG,
    args=None,
    exc_info=None
)


class TestLogHandler:

    def test_requires_correct_properties_if_default_record_factory(self):
        with pytest.raises(TypeError):
            client = _NotALogTable.client('foo')
            QuickbaseLogHandler(client)

    def test_posts_log_record(self, request_spy):
        client = _MyLogsTable.client('foo')
        handler = QuickbaseLogHandler(client)
        _, k = handler._do_emit(MOCK_LOG)
        assert k['json']['data'][0][str(_MyLogsTable.schema.level.fid)]['value'] == MOCK_LOG_LEVEL

    def test_create_with_record_factory(self, request_spy):
        client = _MyLogsTable.client('foo')

        def _mock_rf(record):
            return _MyLogsTable(message=record.msg)

        handler = QuickbaseLogHandler.with_record_factory(client, _mock_rf)
        _, k = handler._do_emit(MOCK_LOG)
        assert str(_MyLogsTable.schema.level.fid) not in k['json']['data'][0]
        assert str(_MyLogsTable.schema.message.fid) in k['json']['data'][0]
