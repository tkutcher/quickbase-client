import requests
from quickbase_client.orm.serialize import QuickBaseJsonEncoder


def quickbase_request(f):
    def _wrap(self, *args, **kwargs):
        request = f(self, *args, **kwargs)
        prepared = request.prepare()
        return self.session.send(prepared)
    return _wrap


class QuickBaseRequestFactory(object):

    def __init__(self, user_token, realm_hostname, agent='python', encoder=QuickBaseJsonEncoder()):
        self.user_token = user_token
        self.realm_hostname = realm_hostname
        self.agent = agent
        self.encoder = encoder

    def make_request(self, method, endpoint, additional_headers=None, params=None, data=None):
        additional_headers = {} if additional_headers is None else additional_headers
        headers = {**self._base_headers(), **additional_headers}
        url = f'https://api.quickbase.com/v1/{endpoint.lstrip("/")}'
        return requests.Request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=self.encoder.encode(data),
            params=params
        )

    def _base_headers(self):
        return {
            'Content-Type': 'application/json',
            'User-Agent': self.agent,
            'Authorization': f'QB-USER-TOKEN {self.user_token}',
            'QB-Realm-Hostname': self.realm_hostname
        }
