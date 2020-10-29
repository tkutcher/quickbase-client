import json
import pathlib

import pytest


def _data_from_file(data_file):
    p = pathlib.Path(__file__).parent / 'data' / data_file
    with open(str(p), 'r') as f:
        return json.load(f)


_mocks = [
    ('GET', '/tables?appId=aaaaaa', 'get_tables.json')
]


@pytest.fixture()
def qb_api_mock(requests_mock):
    for method, endpoint, f in _mocks:
        requests_mock.request(
            method, f'https://api.quickbase.com/v1{endpoint}', json=_data_from_file(f))
