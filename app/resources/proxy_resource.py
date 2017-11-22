import requests
from flask_restful import abort, Resource, reqparse

from . import _data_to_response
from library.gdax_whitelist import is_valid_endpoint
from services.gdax_service_manager import GdaxServiceManager


class ProxyResource(Resource):
    def get(self, endpoint):
        args = self._ensure_request(endpoint)
        service_manager = GdaxServiceManager(args.api_key, args.secret, args.passphrase)
        resp = service_manager.get(endpoint)
        return _data_to_response(resp)

    def delete(self, endpoint):
        args = self._ensure_request(endpoint)
        service_manager = GdaxServiceManager(args.api_key, args.secret, args.passphrase)
        resp = service_manager.delete(endpoint)
        return _data_to_response(resp)

    def options(self, endpoint):
        # CORS...
        self._ensure_valid_endpoint(endpoint)
        return _data_to_response(None)

    @staticmethod
    def _ensure_request(endpoint):
        parser = reqparse.RequestParser()
        parser.add_argument('gdax-api-key', required=True,
                            location='headers', dest='api_key')
        parser.add_argument('gdax-secret', required=True,
                            location='headers', dest='secret')
        parser.add_argument('gdax-passphrase', required=True,
                            location='headers', dest='passphrase')

        args = parser.parse_args()
        ProxyResource._ensure_valid_endpoint(endpoint)
        return args

    @staticmethod
    def _ensure_valid_endpoint(endpoint):
        if not is_valid_endpoint(endpoint):
            abort(403, message='Forbidden endpoint for GET request')
