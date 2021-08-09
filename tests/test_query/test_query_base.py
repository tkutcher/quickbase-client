from quickbase_client.query.query_base import QuickBaseQuery


class TestQuickBaseQuery:
    def test_create(self):
        q = QuickBaseQuery(where="{'18'.EX.19}")
        assert q.where == "{'18'.EX.19}"
