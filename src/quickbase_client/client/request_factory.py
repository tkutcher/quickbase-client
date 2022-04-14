import json

import requests

from quickbase_client.orm.serialize import QuickbaseJsonEncoder


class QuickbaseRequestFactory(object):
    def __init__(
        self,
        user_token,
        realm_hostname,
        agent="python",
        encoder=None,
        allow_deletes=False,
    ):
        self.user_token = user_token
        self.realm_hostname = realm_hostname
        self.agent = agent
        self.encoder = QuickbaseJsonEncoder() if encoder is None else encoder
        self.allow_deletes = allow_deletes
        self.session = requests.Session()

    @property
    def base_headers(self):
        return {
            "Content-Type": "application/json",
            "User-Agent": self.agent,
            "Authorization": f"QB-USER-TOKEN {self.user_token}",
            "QB-Realm-Hostname": self.realm_hostname,
        }

    def make_request(
        self, method, endpoint, additional_headers=None, params=None, data=None
    ) -> requests.Response:
        """Make a request (synchronously) and return the Response.

        :param string method: The (string) HTTP method.
        :param string endpoint: The endpoint of the API (starting after "v1/" for example).
        :param dict additional_headers: A dict of extra headers.
        :param params: Query parameters.
        :param data: The data to send in the body.
        """
        additional_headers = {} if additional_headers is None else additional_headers
        headers = {**self.base_headers, **additional_headers}
        url = f'https://api.quickbase.com/v1/{endpoint.lstrip("/")}'
        if method == "DELETE" and not self.allow_deletes:
            raise RuntimeError("to allow deletes, please set allow_deletes=True")
        # ew - but easiest way to serialize dates
        data = json.loads(self.encoder.encode(data))
        return self.session.request(
            method=method.upper(), url=url, headers=headers, json=data, params=params
        )

    def get(self, endpoint, additional_headers=None, params=None):
        return self.make_request("GET", endpoint, additional_headers, params=params)

    def post(self, endpoint, additional_headers=None, params=None, data=None):
        return self.make_request(
            "POST", endpoint, additional_headers, params=params, data=data
        )

    def delete(self, endpoint, additional_headers=None, data=None):
        return self.make_request("DELETE", endpoint, additional_headers, data=data)


QuickBaseRequestFactory = QuickbaseRequestFactory  # alias - TODO - delete in future
