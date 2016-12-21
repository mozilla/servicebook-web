import requests
import json


def fullname(user):
    firstname = user['firstname'].capitalize()
    lastname = user['lastname'].capitalize()
    return '%s %s' % (firstname, lastname)


class objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]

        raise AttributeError(name)


class DBError(Exception):
    pass


class ServiceBook(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()
        headers = {'Content-Type': 'application/json'}
        self.session.headers.update(headers)

    def _get(self, api, params=None):
        return self.session.get(self.endpoint + api, params=params).json()

    def _patch(self, api, entry_id, data):
        url = self.endpoint +  api + '/%d' % entry_id
        res = self.session.patch(url, data=json.dumps(data))
        if res.status_code != 200:
            try:
                raise DBError(res.json()['message'])
            except (json.decoder.JSONDecodeError, KeyError):
                raise DBError(res.content)

        return res

    def get_entries(self, table, filters=None):
        if filters is None:
            params = {}
        else:
            query = json.dumps({'filters': filters})
            params = {'q': query}
        res = self._get(table, params=params)
        res['objects'] = [objdict(ob) for ob in res['objects']]
        return res

    def update_entry(self, table, data):
        entry_id = data.pop('id')
        return self._patch(table, entry_id, data)

    def get_entry(self, table, entry_id, entry_field='id'):
        filters = [{'name': entry_field, 'op': 'eq', 'val': entry_id}]
        query = json.dumps({'filters': filters})
        params = {'q': query}
        res = self._get(table, params=params)
        return objdict(res['objects'][0])
