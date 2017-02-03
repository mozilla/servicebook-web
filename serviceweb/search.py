import requests


class Search:
    def __init__(self, server):
        self.server = server
        self._q = self.server + 'search?q=%s'

    def __call__(self, query):
        return requests.get(self._q % query).json()
