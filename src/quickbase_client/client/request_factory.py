import requests

from quickbase_client.orm.serialize import QuickBaseJsonEncoder


class QuickBaseRequestFactory(object):

    def __init__(self,
                 user_token,
                 realm_hostname,
                 agent='python',
                 encoder=None,
                 allow_deletes=False):
        self.user_token = user_token
        self.realm_hostname = realm_hostname
        self.agent = agent
        self.encoder = QuickBaseJsonEncoder() if encoder is None else encoder
        self.allow_deletes = allow_deletes

    @property
    def base_headers(self):
        return {
            'Content-Type': 'application/json',
            'User-Agent': self.agent,
            'Authorization': f'QB-USER-TOKEN {self.user_token}',
            'QB-Realm-Hostname': self.realm_hostname
        }

    def make_request(self, method, endpoint, additional_headers=None, params=None, data=None):
        additional_headers = {} if additional_headers is None else additional_headers
        headers = {**self.base_headers, **additional_headers}
        url = f'https://api.quickbase.com/v1/{endpoint.lstrip("/")}'
        if method == 'DELETE' and not self.allow_deletes:
            raise RuntimeError('to allow deletes, please set allow_deletes=True')
        return requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=self.encoder.encode(data),
            params=params
        )

    def get(self, endpoint, additional_headers=None, params=None):
        return self.make_request('GET', endpoint, additional_headers, params=params)

    def post(self, endpoint, additional_headers=None, params=None, data=None):
        return self.make_request('POST', endpoint, additional_headers, params=params, data=data)

    def delete(self, endpoint, additional_headers=None, data=None):
        return self.make_request('DELETE', endpoint, additional_headers, data=data)
