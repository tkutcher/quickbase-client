from typing import Any
from typing import List
from typing import Type
from typing import Union

from quickbase_client.client.api import QuickBaseApiClient
from quickbase_client.orm.field import QuickBaseField
from quickbase_client.orm.report import QuickBaseReport
from quickbase_client.orm.serialize import RecordJsonSerializer
from quickbase_client.orm.table import QuickBaseTable
from quickbase_client.query.query_base import QuickBaseQuery


class QuickBaseTableClient(object):
    """Class for making API calls relative to a specific QuickBase table.

    This includes making calls for the app in general.

    All calls (except :py:meth:`~query`) return a :class:`~requests.Response` object
    for the HTTP response.

    .. note::

        Pagination is not handled in any of these methods (yet).

    :ivar table: The underlying :class:`~QuickBaseTable`
    :ivar api: The wrapped :class:`~QuickBaseApiClient`
    """

    def __init__(self, table: Type[QuickBaseTable], user_token, agent='python'):
        """Create a client instance.

        :param table: The table this client is metaphorically "connected" to.
        :param user_token: The user token to authenticate.
        :param agent: The agent header to send in requests.
        """
        self.table = table
        self.serializer = RecordJsonSerializer(table_cls=self.table)
        self.api = QuickBaseApiClient(user_token, table.realm_hostname(), agent=agent)

    @property
    def app_id(self):
        return self.table.app_id()

    @property
    def table_id(self):
        return self.table.__dbid__

    def get_app(self):
        """Get an app per https://developer.quickbase.com/operation/getApp"""
        return self.api.get_app(self.app_id)

    def get_tables_for_app(self):
        """Get an tables for an app per https://developer.quickbase.com/operation/getAppTables"""
        return self.api.get_tables_for_app(self.app_id)

    def get_table(self):
        """Get a table per https://developer.quickbase.com/operation/getTable"""
        return self.api.get_table(self.app_id, self.table_id)

    def get_fields_for_table(self):
        """Get fields for a table per https://developer.quickbase.com/operation/getFields"""
        return self.api.get_fields_for_table(self.table_id)

    def _get_field_id(self, field: Union[QuickBaseField, int]):
        return field if isinstance(field, int) else field.fid

    def get_field(self, field: Union[QuickBaseField, int]):
        """Get fields for a table per https://developer.quickbase.com/operation/getField

        :param field: either the field ID or a :class:`~QuickBaseField`
        """
        field_id = self._get_field_id(field)
        return self.api.get_field(field_id, self.table_id)

    def get_reports_for_table(self):
        """Get reports for a table per https://developer.quickbase.com/operation/getTableReports"""
        return self.api.get_reports_for_table(self.table_id)

    def _get_report_id(self, report: Union[QuickBaseReport, str, int]):
        return report if isinstance(report, int) else\
            report.report_id if isinstance(report, QuickBaseReport) else \
            self.table.get_report(report).report_id

    def get_report(self, report):
        """Get report  per https://developer.quickbase.com/operation/getReport.

        :param report: Either the report name to lookup, the report id, or a
            :class:`~QuickBaseReport` object.
        """
        report_id = self._get_report_id(report)
        return self.api.get_report(report_id, self.table_id)

    def run_report(self, report, skip=None, top=None):
        """Run report per https://developer.quickbase.com/operation/runReport.

        :param report: Either the report name to lookup, the report id, or a
            :class:`~QuickBaseReport` object.
        """
        report_id = self._get_report_id(report)
        return self.api.run_report(report_id, self.table_id, skip=skip, top=top)

    def _encode_rec(self, rec):
        return self.serializer.serialize(rec) if isinstance(rec, QuickBaseTable) else rec

    def add_records(self, recs: List[Union[QuickBaseTable, Any]], merge_field_id=None,
                    fields_to_return=None):
        """Add record per https://developer.quickbase.com/operation/upsert.

        :param recs: A list of items that are either the raw record data to post, or the
            :class:`~QuickBaseTable` object/record.
        :param merge_field_id: The list of fields to merge on.
        :param fields_to_return: The list of field ID's to return (default None which means all).
        """
        data = [self._encode_rec(rec) for rec in recs]
        return self.api.add_records(
            table_id=self.table_id,
            data=data,
            merge_field_id=merge_field_id,
            fields_to_return=fields_to_return)

    def add_record(self, rec, *args, **kwargs):
        """Aliased to :meth:`~add_records` making rec a list."""
        return self.add_records([rec], *args, **kwargs)

    def query(self, query_obj: QuickBaseQuery = None, raw=False):
        """Do a query per https://developer.quickbase.com/operation/runQuery.

        See :mod:`~quickbase_client.query` for more.

        :param query_obj: The :class:`~QuickBaseQuery` object to use.
        :param raw: If true, returns a requests.Response, else the data is serialized to a table
            object.
        """
        query_obj = QuickBaseQuery(where=None) if query_obj is None else query_obj
        data = self.api.query(
            table_id=self.table_id,
            fields_to_select=query_obj.select,
            where_str=query_obj.where,
            sort_by=query_obj.sort_by,
            group_by=query_obj.group_by,
            options=query_obj.options)
        return data if raw else [self.serializer.deserialize(x) for x in data.json()['data']]
