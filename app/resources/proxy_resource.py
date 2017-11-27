from flask import request
from flask_restful import abort, Resource, reqparse

from . import _data_to_response
from library.gdax_whitelist import is_valid_endpoint
from services.gdax_service_manager import GdaxServiceManager


class ProxyResource(Resource):
    def delete(self, endpoint):
        return self._proxy_request(endpoint)

    def get(self, endpoint):
        return self._proxy_request(endpoint)

    def post(self, endpoint):
        return self._proxy_request(endpoint)

    def put(self, endpoint):
        return self._proxy_request(endpoint)

    def options(self, endpoint):
        # CORS...
        self._ensure_valid_endpoint(endpoint)
        return _data_to_response(None)

    def _proxy_request(self, endpoint):
        args = self._ensure_request(endpoint)
        service_manager = GdaxServiceManager(args.api_key, args.secret, args.passphrase)

        if request.method == 'GET':
            resp = service_manager.get(endpoint)
        elif request.method == 'POST':
            resp = service_manager.post(endpoint, request.data)
        elif request.method == 'PUT':
            resp = service_manager.put(endpoint, request.data)
        elif request.method == 'DELETE':
            resp = service_manager.delete(endpoint)
        else:
            resp = None

        return _data_to_response(resp)

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
            abort(403, message='Forbidden endpoint')
