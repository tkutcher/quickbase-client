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

    def __init__(self, table: Type[QuickBaseTable], user_token, agent='python'):
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
        return self.api.get_app(self.app_id)

    def get_tables_for_app(self):
        return self.api.get_tables_for_app(self.app_id)

    def get_table(self):
        return self.api.get_table(self.app_id, self.table_id)

    def get_fields_for_table(self):
        return self.api.get_fields_for_table(self.table_id)

    def _get_field_id(self, field: Union[QuickBaseField, int]):
        return field if isinstance(field, int) else field.fid

    def get_field(self, field: Union[QuickBaseField, int]):
        field_id = self._get_field_id(field)
        return self.api.get_field(field_id, self.table_id)

    def get_reports_for_table(self):
        return self.api.get_reports_for_table(self.table_id)

    def _get_report_id(self, report: Union[QuickBaseReport, str, int]):
        return report if isinstance(report, int) else\
            report.report_id if isinstance(report, QuickBaseReport) else \
            self.table.get_report(report).report_id

    def get_report(self, report):
        report_id = self._get_report_id(report)
        return self.api.get_report(report_id, self.table_id)

    def run_report(self, report, skip=None, top=None):
        report_id = self._get_report_id(report)
        return self.api.run_report(report_id, self.table_id, skip=skip, top=top)

    def _encode_rec(self, rec):
        return self.serializer.serialize(rec) if isinstance(rec, QuickBaseTable) else rec

    def add_records(self, recs: List[Union[QuickBaseTable, Any]], merge_field_id=None,
                    fields_to_return=None):
        data = [self._encode_rec(rec) for rec in recs]
        return self.api.add_records(
            table_id=self.table_id,
            data=data,
            merge_field_id=merge_field_id,
            fields_to_return=fields_to_return)

    def add_record(self, rec, *args, **kwargs):
        return self.add_records([rec], *args, **kwargs)

    def query(self, query_obj: QuickBaseQuery = None, raw=False):
        query_obj = QuickBaseQuery(where=None) if query_obj is None else query_obj
        data = self.api.query(
            table_id=self.table_id,
            fields_to_select=query_obj.select,
            where_str=query_obj.where,
            sort_by=query_obj.sort_by,
            group_by=query_obj.group_by,
            options=query_obj.options)
        return data if raw else [self.serializer.deserialize(x) for x in data.json()['data']]
