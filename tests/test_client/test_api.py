from quickbase_client.client.api import QuickBaseApiClient


class TestQuickBaseApiClient(object):
    """
    The majority of interesting things are tested via the higher-level table-client.
    """

    def test_makes_request_factory(self):
        client = QuickBaseApiClient(user_token='foo', realm_hostname='dicorp.quickbase.com')
        assert client.rf.user_token == 'foo'
        assert client.rf.realm_hostname == 'dicorp.quickbase.com'
