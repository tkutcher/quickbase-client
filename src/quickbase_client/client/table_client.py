from typing import Any
from typing import List
from typing import Type
from typing import Union

from quickbase_client import ResponsePager
from quickbase_client.client.api import QuickbaseApiClient
from quickbase_client.orm.field import QuickbaseField
from quickbase_client.orm.report import QuickbaseReport
from quickbase_client.orm.serialize import RecordJsonSerializer
from quickbase_client.orm.table import QuickbaseTable
from quickbase_client.query.query_base import QuickbaseQuery


class QuickbaseTableClient(object):
    """Class for making API calls relative to a specific QuickBase table.

    This includes making calls for the app in general.

    All calls (except :py:meth:`~query`) return a :class:`~requests.Response` object
    for the HTTP response.

    .. note::

        Pagination is not handled in any of these methods (yet).

    :ivar table:
        The underlying :class:`~QuickbaseTable`

    :ivar api:
        The wrapped :class:`~QuickbaseApiClient`

    :param user_token:
        The user token to authenticate.

    :param agent:
        The agent header to send in requests.

    :param normalize_unicode:
        Whether the JSON Serializer should normalize accented characters so that they
        can be encoded in Quickbase.

    :param bool allow_deletes:
        Whether the client should be allowed to perform delete requests. Defaulted to
        False for now. But note that this is subject to change in 1.0 if there is a
        different general preference.
    """

    def __init__(
        self,
        table: Type[QuickbaseTable],
        user_token,
        agent="python",
        normalize_unicode=True,
        allow_deletes=False,
    ):
        self.table = table
        self.serializer = RecordJsonSerializer(
            table_cls=self.table, normalize_unicode=normalize_unicode
        )
        self.api = QuickbaseApiClient(
            user_token,
            table.realm_hostname(),
            agent=agent,
            allow_deletes=allow_deletes,
        )

    @property
    def app_id(self):
        return self.table.app_id()

    @property
    def table_id(self):
        return self.table.__dbid__

    def get_app(self):
        """Get an app.

        https://developer.quickbase.com/operation/getApp
        """
        return self.api.get_app(self.app_id)

    def get_tables_for_app(self):
        """Get an tables for an app.

        https://developer.quickbase.com/operation/getAppTables
        """
        return self.api.get_tables_for_app(self.app_id)

    def get_table(self):
        """Get a table.

        https://developer.quickbase.com/operation/getTable
        """
        return self.api.get_table(self.app_id, self.table_id)

    def get_fields_for_table(self):
        """Get fields for a table.

        https://developer.quickbase.com/operation/getFields
        """
        return self.api.get_fields_for_table(self.table_id)

    @staticmethod
    def _get_field_id(field: Union[QuickbaseField, int]):
        return field if isinstance(field, int) else field.fid

    def get_field(self, field: Union[QuickbaseField, int]):
        """Get fields for a table.

        https://developer.quickbase.com/operation/getField

        :param field: either the field ID or a :class:`~QuickbaseField`
        """
        field_id = self._get_field_id(field)
        return self.api.get_field(field_id, self.table_id)

    def get_reports_for_table(self):
        """Get reports for a table.

        https://developer.quickbase.com/operation/getTableReports
        """
        return self.api.get_reports_for_table(self.table_id)

    def _get_report_id(self, report: Union[QuickbaseReport, str, int]):
        return (
            report
            if isinstance(report, int)
            else report.report_id
            if isinstance(report, QuickbaseReport)
            else self.table.get_report(report).report_id
        )

    def get_report(self, report):
        """Get report.

        https://developer.quickbase.com/operation/getRepor

        :param report: Either the report name to lookup, the report id, or a
            :class:`~QuickbaseReport` object.
        """
        report_id = self._get_report_id(report)
        return self.api.get_report(report_id, self.table_id)

    def run_report(self, report, skip=None, top=None):
        """Run report.

        https://developer.quickbase.com/operation/runReport.

        :param report:
            Either the report name to lookup, the report id, or a
            :class:`~QuickbaseReport` object.

        :param int skip:
            For paging (see Quickbase API)

        :param int top:
            For paging (see Quickbase API)
        """
        report_id = self._get_report_id(report)
        return self.api.run_report(report_id, self.table_id, skip=skip, top=top)

    def _encode_rec(self, rec):
        return (
            self.serializer.serialize(rec) if isinstance(rec, QuickbaseTable) else rec
        )

    def add_records(
        self,
        recs: List[Union[QuickbaseTable, Any]],
        merge_field_id=None,
        fields_to_return=None,
    ):
        """Add record.

        https://developer.quickbase.com/operation/upsert

        :param recs:
            A list of items that are either the raw record data to post, or the
            :class:`~QuickbaseTable` object/record.

        :param merge_field_id:
            The list of fields to merge on.

        :param fields_to_return:
            The list of field ID's to return (default None which means all).
        """
        data = [self._encode_rec(rec) for rec in recs]
        return self.api.add_records(
            table_id=self.table_id,
            data=data,
            merge_field_id=merge_field_id,
            fields_to_return=fields_to_return,
        )

    def add_record(self, rec, *args, **kwargs):
        """Aliased to :meth:`~add_records` making rec a list."""
        return self.add_records([rec], *args, **kwargs)

    def query(
        self, query_obj: QuickbaseQuery = None, raw=False, pager: ResponsePager = None
    ):
        """Do a query.

        https://developer.quickbase.com/operation/runQuery.

        See :mod:`~quickbase_client.query` for more.

        See :class:`~quickbase_client.ResponsePager` for handling pagination.

        If some fields are coming back as null, a common "gotcha" is that the
        Quickbase API by default only returns fields listed as "default" in a table.
        In that case you would have to explicitly specify a ``select`` in the
        query, or you can edit the fields in Quickbase to be default fields.

        :param query_obj:
            The :class:`~QuickbaseQuery` object to use. Note that this object also
            specifies the ``select``, ``group_by``, ``sort_by``, etc. So to specify
            those you need to specify them in the provided :class:`~QuickbaseQuery`.
            See its documentation for more details.

        :param raw:
            If true, returns a requests.Response, else the data is
            serialized to a table object.

        :param pager:
            A :class:`~ResponsePager` to handle making paginated requests.
        """
        pager = ResponsePager() if pager is None else pager
        query_obj = QuickbaseQuery(where=None) if query_obj is None else query_obj
        options = pager.get_options()
        options = {**options, **(query_obj.options if query_obj.options else {})}
        data = self.api.query(
            table_id=self.table_id,
            fields_to_select=query_obj.select,
            where_str=query_obj.where,
            sort_by=query_obj.sort_by,
            group_by=query_obj.group_by,
            options=options,
        )
        pager.update_from_metadata(data.json()["metadata"])
        return (
            data
            if raw
            else [self.serializer.deserialize(x) for x in data.json()["data"]]
        )

    def change_record_owner(self, rid, new_owner):
        """Use the legacy API to change a Record's owner.

        See https://help.quickbase.com/api-guide/change_record_owner.html

        :param rid:
            The record ID to change the owner of

        :param new_owner:
            The email address, or user ID, of the user to change to the owner.
        """
        return self.api.legacy_api.change_record_owner(self.table_id, rid, new_owner)


QuickBaseTableClient = QuickbaseTableClient  # alias - TODO - delete in future
