from quickbase_client.query.query_base import QuickbaseQuery


class TestQuickbaseQuery:
    def test_create(self):
        q = QuickbaseQuery(where="{'18'.EX.19}")
        assert q.where == "{'18'.EX.19}"
