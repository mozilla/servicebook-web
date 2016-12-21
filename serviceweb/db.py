import requests
import json


class ServiceBook(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()
        headers = {'Content-Type': 'application/json'}
        self.session.headers.update(headers)

    def _get(self, api, params=None):
        return self.session.get(self.endpoint + api, params=params).json()

    def get_entries(self, table, filters=None):
        if filters is None:
            params = {}
        else:
            query = json.dumps({'filters': filters})
            params = {'q': query}
        res = self._get(table, params=params)
        return res

    def get_entry(self, table, entry_id):
        filters = [{'name': 'id', 'op': 'eq', 'val': entry_id}]
        query = json.dumps({'filters': filters})
        params = {'q': query}
        res = self._get(table, params=params)
        return res['objects'][0]
