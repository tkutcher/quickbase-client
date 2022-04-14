import pytest
import requests

from quickbase_client.client.request_factory import QuickbaseRequestFactory


class TestQuickbaseRequestFactory:
    def test_no_real_requests_are_made(self):
        """For internal framework mostly"""
        assert requests.get("https://anvilorsolutions.com").json() == {}

    def test_includes_auth_header(self, mocker):
        rf = QuickbaseRequestFactory(user_token="foo", realm_hostname="x.quickbase.com")
        spy = mocker.spy(rf.session, "request")
        rf.get("/bleh")
        args, kwargs = spy.call_args
        headers = kwargs["headers"]
        assert "Authorization" in headers
        assert headers["Authorization"] == "QB-USER-TOKEN foo"

    def test_extra_headers(self, mocker):
        rf = QuickbaseRequestFactory(user_token="foo", realm_hostname="x.quickbase.com")
        spy = mocker.spy(rf.session, "request")
        rf.get("/bleh", additional_headers={"a": "b"})
        args, kwargs = spy.call_args
        assert "a" in kwargs["headers"]
        assert kwargs["headers"]["a"] == "b"

    def test_make_delete(self, mocker):
        rf = QuickbaseRequestFactory(
            user_token="foo", realm_hostname="x.quickbase.com", allow_deletes=True
        )
        spy = mocker.spy(rf.session, "request")
        rf.delete("/bleh")
        args, kwargs = spy.call_args
        assert kwargs["method"] == "DELETE"

    def test_cannot_delete_by_default(self):
        rf = QuickbaseRequestFactory(user_token="foo", realm_hostname="x.quickbase.com")
        with pytest.raises(RuntimeError):
            rf.delete("/bleh")
