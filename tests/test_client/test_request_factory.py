import pytest

from quickbase_client.client.request_factory import QuickBaseRequestFactory


class TestRequestFactory:
    def test_includes_auth_header(self, request_spy):
        rf = QuickBaseRequestFactory(user_token="foo", realm_hostname="x.quickbase.com")
        args, kwargs = rf.get("/bleh")
        headers = kwargs["headers"]
        assert "Authorization" in headers
        assert headers["Authorization"] == "QB-USER-TOKEN foo"

    def test_extra_headers(self, request_spy):
        rf = QuickBaseRequestFactory(user_token="foo", realm_hostname="x.quickbase.com")
        args, kwargs = rf.get("/bleh", additional_headers={"a": "b"})
        assert "a" in kwargs["headers"]
        assert kwargs["headers"]["a"] == "b"

    def test_make_delete(self, request_spy):
        rf = QuickBaseRequestFactory(
            user_token="foo", realm_hostname="x.quickbase.com", allow_deletes=True
        )
        args, kwargs = rf.delete("/bleh")
        assert kwargs["method"] == "DELETE"

    def test_cannot_delete_by_default(self, request_spy):
        rf = QuickBaseRequestFactory(user_token="foo", realm_hostname="x.quickbase.com")
        with pytest.raises(RuntimeError):
            rf.delete("/bleh")
