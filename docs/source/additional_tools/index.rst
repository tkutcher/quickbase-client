====================
Additional Tools
====================


Sending logs to Quickbase with QuickbaseLogHandler
--------------------------------------------------

It is often appropriate to send some logs to Quickbase, especially when writing scripts that
interface with Quickbase. This package includes a log handler as part of Python standard logging,
that will send logs in the background.

You supply it with a table client to the logs table, and the handler will send logs to that
table in a non-blocking background thread.

By default, the class assumes the table has attributes for "when", "level", and "message". You
can supply a custom record factory via passing a function to `with_record_factory`, or
by extending this class and overriding `record_factory`.

For example, say you have a QuickBaseTable class called MyLog. You can create a class like so:

.. code:: python

    class InvocationLog(QuickBaseTable):
        __dbid__ = 'abcdef'
        __app__ = QuickBaseApp(app_id='aaappp', name='APP', realm_hostname='foo.quickbase.com')

        date_created = QuickBaseField(fid=1, field_type=Qb.DATETIME)
        date_modified = QuickBaseField(fid=2, field_type=Qb.DATETIME)
        recordid = QuickBaseField(fid=3, field_type=Qb.NUMERIC)
        record_owner = QuickBaseField(fid=4, field_type=Qb.USER)
        last_modified = QuickBaseField(fid=5, field_type=Qb.USER)

        log_message = QuickBaseField(fid=6, field_type=Qb.TEXT)
        logged_when = QuickBaseField(fid=7, field_type=Qb.DATETIME)


   class MyLogHandler(QuickbaseLogHandler):
       def __init__(self):
           super().__init__(MyLog.client(my_user_token))

       def record_factory(self, record: logging.LogRecord):
           return MyLog(log_message=record.msg, logged_when=datetime.utcnow())


   logger = logging.getLogger()
   logger.addHandler(MyLogHandler())
   logger.info('This message should show up in Quickbase!')


|

.. autoclass:: quickbase_client.tools.QuickbaseLogHandler
    :members:

|
