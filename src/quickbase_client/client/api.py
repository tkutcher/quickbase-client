from quickbase_client.client.request_factory import QuickBaseRequestFactory


def make_payload(d):
    return {k: v for k, v in d.items() if v is not None}


class QuickBaseApiClient(object):
    """The lower-level client to make API requests.

    Use :meth:`~request` to make an arbitrary request that forwards to
    :meth:`~QuickBaseRequestFactory.make_request`
    """

    def __init__(self, user_token, realm_hostname, agent='python', allow_deletes=False):
        self.rf = QuickBaseRequestFactory(
            user_token,
            realm_hostname,
            agent,
            allow_deletes=allow_deletes
        )

    def request(self, *args, **kwargs):
        return self.rf.make_request(*args, **kwargs)

    # FUTURE - Can add more of these methods, even refactoring in to separate classes for each
    #   main endpoint. Initially just including some of the more common functions.

    def get_app(self, app_id):
        return self.rf.get(f'/apps/{app_id}')

    def get_tables_for_app(self, app_id):
        return self.rf.get('/tables', params={'appId': app_id})

    def get_table(self, app_id, table_id):
        return self.rf.get(f'/tables/{table_id}', params={'appId': app_id})

    def get_fields_for_table(self, table_id):
        return self.rf.get('/fields', params={'tableId': table_id})

    def get_field(self, field_id, table_id):
        return self.rf.get(f'/fields/{field_id}', params={'tableId': table_id})

    def get_reports_for_table(self, table_id):
        return self.rf.get('/reports', params={'tableId': table_id})

    def get_report(self, report_id, table_id):
        return self.rf.get(f'/reports/{report_id}', params={'tableId': table_id})

    def run_report(self, report_id, table_id, skip=None, top=None):
        payload = make_payload({'skip': skip, 'top': top})
        return self.rf.post(f'/reports/{report_id}/run', params={'tableId': table_id},
                            data=payload)

    def add_records(self, table_id, data=None, merge_field_id=None, fields_to_return=None):
        return self.rf.post('/records', data=make_payload({
            'to': table_id,
            'data': data,
            'mergeFieldId': merge_field_id,
            'fieldsToReturn': fields_to_return
        }))

    def query(self, table_id, fields_to_select=None, where_str=None, sort_by=None, group_by=None,
              options=None):
        return self.rf.post('/records/query', data=make_payload({
            'from': table_id,
            'select': fields_to_select,
            'where': where_str,
            'sortBy': sort_by,
            'groupBy': group_by,
            'options': options
        }))
