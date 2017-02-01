import requests


class Mozillians(object):
    def __init__(self, app):
        self.endpoint = app.config['mozillians']['endpoint']
        self.key = app.config['mozillians']['api_key']
        self._cache = {}
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['mozillians'] = self

    def get_info(self, username):
        if username in self._cache:
            url = self._cache[username]
        else:
            url = '?api-key=%s&username=%s&format=json'
            url = url % (self.key, username)
            try:
                user = requests.get(self.endpoint + url).json()
            except requests.exceptions.SSLError:
                return {}

            if 'results' not in user:
                return {}

            res = user['results']
            if len(res) == 0:
                return {}

            url = res[0]['_url']
            self._cache[username] = url

        url = url + '?api-key=%s&format=json'
        url = url % self.key
        try:
            details = requests.get(url).json()
        except requests.exceptions.SSLError:
            return {}
        return details
