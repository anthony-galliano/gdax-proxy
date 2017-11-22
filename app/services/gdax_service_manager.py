import requests

from library.gdax_auth import GdaxAuth

BASE_URL = 'https://api.gdax.com{}'


class GdaxServiceManager:
    def __init__(self, api_key, secret, passphrase):
        self.auth = GdaxAuth(api_key, secret, passphrase)

    def get(self, endpoint):
        return requests.get(BASE_URL.format(endpoint), auth=self.auth)

    def post(self, endpoint, data=None):
        return requests.post(BASE_URL.format(endpoint), data=data, auth=self.auth)

    def put(self, endpoint, data=None):
        return requests.put(BASE_URL.format(endpoint), data=data, auth=self.auth)

    def delete(self, endpoint):
        return requests.delete(BASE_URL.format(endpoint), auth=self.auth)
