from quickbase_client.client.legacy_client import QuickbaseLegacyApiClient


class TestQuickbaseLegacyApiClient:
    def test_make_request_includes_action_in_header(self, mocker):
        client = QuickbaseLegacyApiClient("whocares", "foo.quickbase.com")
        spy = mocker.spy(client.session, "request")
        client.make_request(
            "POST", "API_DoSomething", endpoint="/db/foo", request_data_xml_str=""
        )
        args, kwargs = spy.call_args
        headers = kwargs["headers"]
        assert headers["QUICKBASE-ACTION"] == "API_DoSomething"
        assert headers["Content-Type"] == "application/xml"

    def test_make_request_includes_token(self, mocker):
        client = QuickbaseLegacyApiClient("whocares", "foo.quickbase.com")
        spy = mocker.spy(client.session, "request")
        client.make_request(
            "POST", "API_DoSomething", endpoint="/db/foo", request_data_xml_str=""
        )
        args, kwargs = spy.call_args
        data = kwargs["data"]
        assert "<usertoken>whocares" in data

    def test_change_record_owner_calls_properly(self, mocker):
        client = QuickbaseLegacyApiClient("whocares", "foo.quickbase.com")
        spy = mocker.spy(client.session, "request")
        client.change_record_owner("abc", 6, "tkutcher")
        args, kwargs = spy.call_args
        headers = kwargs["headers"]
        assert headers["QUICKBASE-ACTION"] == "API_ChangeRecordOwner"
        assert kwargs["url"] == "https://foo.quickbase.com/db/abc"
        assert "<rid>6" in kwargs["data"]
        assert "<newowner>tkutcher" in kwargs["data"]

    def test_make_request_returns_response(self, mocker):
        client = QuickbaseLegacyApiClient("whocares", "foo.quickbase.com")
        request_mock = mocker.patch.object(client.session, "request")
        mock_xml_response = """
            <?xml version="1.0" ?>
            <qdbapi>
                <action>API_FooTest</action>
            </qdbapi>
        """
        request_mock.return_value.text = mock_xml_response

        response = client.make_request(
            "POST", "API_FooTest", endpoint="/db/foo", request_data_xml_str=""
        )
        assert response.text == mock_xml_response
        assert request_mock.call_count == 1
