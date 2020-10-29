from quickbase_client.client.table_client import QuickBaseTableClient


def test_makes_request(qb_api_mock, example_table):
    client = QuickBaseTableClient(example_table, user_token='anything')
    r = client.get_all_app_tables()
    assert len(r.json()) == 1
