import json

from quickbase_client.client.api import QuickbaseApiClient


class TestQuickbaseApiClient(object):
    """
    The majority of interesting things are tested via the higher-level table-client.
    """

    def test_makes_request_factory(self):
        client = QuickbaseApiClient(
            user_token="foo", realm_hostname="dicorp.quickbase.com"
        )
        assert client._rf.user_token == "foo"
        assert client._rf.realm_hostname == "dicorp.quickbase.com"

    def test_request_alias(self, mocker):
        client = QuickbaseApiClient(
            user_token="foo", realm_hostname="dicorp.quickbase.com"
        )
        spy = mocker.spy(client._rf.session, "request")
        client.request(method="POST", endpoint="/blah")
        _, kwargs = spy.call_args
        assert kwargs["method"] == "POST"

    def test_class_is_aliases(self, mocker):
        from quickbase_client.client.api import QuickBaseApiClient

        client = QuickBaseApiClient(
            user_token="foo", realm_hostname="dicorp.quickbase.com"
        )
        spy = mocker.spy(client._rf.session, "request")
        client.request(method="POST", endpoint="/blah")
        _, kwargs = spy.call_args
        assert kwargs["method"] == "POST"

    def test_query(self, mocker):
        client = QuickbaseApiClient(
            user_token="foo", realm_hostname="dicorp.quickbase.com"
        )
        spy = mocker.spy(client._rf.session, "request")
        client.query(table_id="aaaaaa", where_str="{'18'.EX.19}")
        _, kwargs = spy.call_args
        assert "{'18'.EX.19}" in json.dumps(kwargs["json"])
