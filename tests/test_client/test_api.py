from quickbase_client.client.api import QuickBaseApiClient


class TestQuickBaseApiClient(object):
    """
    The majority of interesting things are tested via the higher-level table-client.
    """

    def test_makes_request_factory(self):
        client = QuickBaseApiClient(user_token='foo', realm_hostname='dicorp.quickbase.com')
        assert client.rf.user_token == 'foo'
        assert client.rf.realm_hostname == 'dicorp.quickbase.com'

    def test_request_alias(self, request_spy):
        client = QuickBaseApiClient(user_token='foo', realm_hostname='dicorp.quickbase.com')
        _, kwargs = client.request(method='POST', endpoint='/blah')
        assert kwargs['method'] == 'POST'

    def test_query(self, request_spy):
        client = QuickBaseApiClient(user_token='foo', realm_hostname='dicorp.quickbase.com')
        _, kwargs = client.query(table_id='aaaaaa', where_str="{'18'.EX.19}")
        assert "{'18'.EX.19}" in kwargs['json']
