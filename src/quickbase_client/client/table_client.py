from typing import Type

from quickbase_client.client.api_client import QuickBaseApiClient
from quickbase_client.orm.table import QuickBaseTable


class QuickBaseTableClient(object):

    def __init__(self, table: Type[QuickBaseTable], user_token, agent='python'):
        self.table = table
        self.api = QuickBaseApiClient(user_token, table.app.realm_hostname, agent=agent)

    def get_all_app_tables(self):
        return self.api.get_tables_for_app(self.table.app.app_id)

    def get_fields(self):
        return self.api.get_fields_for_table(self.table.__dbid__)
