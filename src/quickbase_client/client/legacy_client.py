import requests

from quickbase_client.utils.string_utils import normalize_hostname


class QuickbaseLegacyApiClient:
    """Legacy Client which makes requests to the old XML API.

    This operates more generically to send any request to the old API. It's primary
    purpose is to supplement the JSON API for things not yet supported.

    It does include some higher-level methods for things that in particular are
    not supported in the new API's. If there are others you would like added,
    submit an Issue or a Merge-Request and we can certainly add it!

    Rather than get in to having lxml as an optional dependency, it will just deal
    with XML data as strings for now. If we want more support of the XML API, then
    it might be worth it to introduce that.

    :param str user_token:
        The user token for authenticating with the API. Note that the other forms of
        authentication through the XML API are not supported via this library.


    :param str realm_hostname:
        The hostname - like ``"foo.quickbase.com"``

    """

    def __init__(self, user_token: str, realm_hostname: str):
        self.user_token = user_token
        self.realm_hostname = normalize_hostname(realm_hostname)
        self.session = requests.Session()

    def make_request(
        self,
        http_method: str,
        quickbase_action: str,
        endpoint: str,
        request_data_xml_str="",
    ):
        """Used as a simple Python interface to the old XML API.

        :param str http_method:
            The HTTP method, like ``"post"``

        :param str quickbase_action:
            The Quickbase Action to send, like ``"API_ChangeRecordOwner"``

        :param str endpoint:
            The HTTP Endpoint to call, like ``/db/abc123``

        :param str request_data_xml_str:
            The data to add to the XML string that gets sent, *inside* of the
            ``qdbapi`` element/tag. For now this is all done through strings, in the
            future it may use lxml and have better capabilities for working with
            those trees.
        """

        data_xml = f"""
        <qdbapi>
           <usertoken>{self.user_token}</usertoken>
           {request_data_xml_str}
        </qdbapi>
        """
        headers = {
            "Content-Type": "application/xml",
            "QUICKBASE-ACTION": quickbase_action,
        }
        url = f"https://{self.realm_hostname}/{endpoint.lstrip('/')}"
        self.session.request(
            method=http_method,
            url=url,
            headers=headers,
            data=data_xml,
        )

    # Common Use Cases:

    def change_record_owner(self, table_id, rid, new_owner):
        """The Quickbase API_ChangeRecordOwner action

        See https://help.quickbase.com/api-guide/change_record_owner.html

        :param table_id:
            The table ID containing the record

        :param rid:
            The record ID to change the owner of

        :param new_owner:
            The email address, or user ID, of the user to change to the owner.
        """
        return self.make_request(
            http_method="POST",
            quickbase_action="API_ChangeRecordOwner",
            endpoint=f"/db/{table_id}",
            request_data_xml_str=f"""
                <rid>{rid}</rid>
                <newowner>{new_owner}</newowner>
            """,
        )
