import json
import pathlib

import pytest

from quickbase_client.client import request_factory

@pytest.fixture()
def request_spy(monkeypatch):
    def _spy(*args_, **kwargs_):
        return args_, kwargs_
    monkeypatch.setattr(request_factory.requests, 'request', _spy)
