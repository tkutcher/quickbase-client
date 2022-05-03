from quickbase_client.client.legacy_client import QuickbaseLegacyApiClient
from quickbase_client.client.request_factory import QuickbaseRequestFactory


def make_payload(d):
    return {k: v for k, v in d.items() if v is not None}


class QuickbaseApiClient(object):
    """The lower-level client to make API requests.

    .. note::
        Current alias of ``QuickBaseApiClient`` for backwards compatibility - will be
        removed in version 1.0

    Use :meth:`~request` to make an arbitrary request that forwards to
    :meth:`~QuickbaseRequestFactory.make_request`

    :ivar legacy_api:
        The :class:`~QuickbaseLegacyApiClient` for making requests to the XML API.
    """

    def __init__(self, user_token, realm_hostname, agent="python", allow_deletes=False):
        self._rf = QuickbaseRequestFactory(
            user_token, realm_hostname, agent, allow_deletes=allow_deletes
        )
        self.legacy_api = QuickbaseLegacyApiClient(user_token, realm_hostname)

    def request(self, *args, **kwargs):
        return self._rf.make_request(*args, **kwargs)

    # FUTURE - Can add more of these methods, even refactoring in to separate classes
    #   for each main endpoint. Initially just including some of the more common
    #   functions.

    def get_app(self, app_id):
        return self._rf.get(f"/apps/{app_id}")

    def get_tables_for_app(self, app_id):
        return self._rf.get("/tables", params={"appId": app_id})

    def get_table(self, app_id, table_id):
        return self._rf.get(f"/tables/{table_id}", params={"appId": app_id})

    def get_fields_for_table(self, table_id):
        return self._rf.get("/fields", params={"tableId": table_id})

    def get_field(self, field_id, table_id):
        return self._rf.get(f"/fields/{field_id}", params={"tableId": table_id})

    def get_reports_for_table(self, table_id):
        return self._rf.get("/reports", params={"tableId": table_id})

    def get_report(self, report_id, table_id):
        return self._rf.get(f"/reports/{report_id}", params={"tableId": table_id})

    def run_report(self, report_id, table_id, skip=None, top=None):
        payload = make_payload({"skip": skip, "top": top})
        return self._rf.post(
            f"/reports/{report_id}/run", params={"tableId": table_id}, data=payload
        )

    def add_records(
        self, table_id, data=None, merge_field_id=None, fields_to_return=None
    ):
        return self._rf.post(
            "/records",
            data=make_payload(
                {
                    "to": table_id,
                    "data": data,
                    "mergeFieldId": merge_field_id,
                    "fieldsToReturn": fields_to_return,
                }
            ),
        )

    def query(
        self,
        table_id,
        fields_to_select=None,
        where_str=None,
        sort_by=None,
        group_by=None,
        options=None,
    ):
        return self._rf.post(
            "/records/query",
            data=make_payload(
                {
                    "from": table_id,
                    "select": fields_to_select,
                    "where": where_str,
                    "sortBy": sort_by,
                    "groupBy": group_by,
                    "options": options,
                }
            ),
        )


QuickBaseApiClient = QuickbaseApiClient  # alias - TODO - delete in future
