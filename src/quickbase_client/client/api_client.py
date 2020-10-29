from quickbase_client.client.request_factory import quickbase_request
from quickbase_client.client.request_factory import QuickBaseRequestFactory
from requests import Session


class QuickBaseApiClient(object):

    def __init__(self, user_token, realm_hostname, agent='python'):
        self.session = Session()
        self.request_factory = QuickBaseRequestFactory(user_token, realm_hostname, agent)

    @quickbase_request
    def get_tables_for_app(self, app_id):
        return self.request_factory.make_request('GET', '/tables', params={'appId': app_id})

    @quickbase_request
    def get_fields_for_table(self, dbid):
        return self.request_factory.make_request('GET', '/fields', params={'tableId': dbid})

