import logging
import threading
from datetime import datetime

from quickbase_client import QuickbaseTableClient

_mock_record = logging.LogRecord(
    name="", level=0, pathname="", lineno=1, msg="", args=None, exc_info=None
)


class QuickbaseLogHandler(logging.Handler):
    """Class for sending logs to a specific Quickbase table.

    You supply it with a table client to the logs table, and the handler will send logs
    to that table in a non-blocking background thread.

    This uses the higher-level QuickbaseTableClient APIs. So you will have to
    create a class for your table you want to send logs to.
    """

    def __init__(self, logs_table_client: QuickbaseTableClient):
        self.client = logs_table_client

        try:
            self.record_factory(_mock_record)
        except Exception:
            raise TypeError(
                "Invalid record_factory - could not create a log record. If using"
                'the default, either ensure your table has properties "when", '
                '"level", and "message", OR implement a custom record_factory.'
            )

        super().__init__()

    @staticmethod
    def with_record_factory(logs_table_client: QuickbaseTableClient, record_factory):
        """Create a logger using a function to make records.

        :param logs_table_client:
            The QuickbaseTableClient for the logs to go to.

        :param record_factory:
            A function which takes a `logging.LogRecord` and creates the relevant
            record (instance of a :class:`~QuickbaseTable`).
        """

        class _CustomRecordFactoryHandler(QuickbaseLogHandler):
            def record_factory(self, record: logging.LogRecord):
                return record_factory(record)

        return _CustomRecordFactoryHandler(logs_table_client)

    def record_factory(self, record: logging.LogRecord):
        """
        Create a :class:`~QuickbaseTable` record object given a LogRecord. By default,
        this assumes the associated table, under the handlers table client, has
        properties ``when``, ``level``, and ``message``.

        :param record: The logging.LogRecord.
        :return: A QuickbaseTable record object.
        """
        return self.client.table(
            when=datetime.utcnow(),
            level=record.levelno,
            message=record.msg,
        )

    def emit(self, record):
        """Calls :meth:`~record_factory` and starts a thread to send it to Quickbase."""
        t = threading.Thread(target=self._do_emit, args=[record])
        t.start()

    def _do_emit(self, record):
        qb_rec = self.record_factory(record)
        return self.client.add_record(qb_rec)
