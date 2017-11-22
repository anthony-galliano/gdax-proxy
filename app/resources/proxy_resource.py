from flask_restful import abort, Resource, reqparse
from ratelimit import rate_limited

from . import _data_to_response
from library.gdax_whitelist import is_valid_get_endpoint
from services.gdax_service_manager import GdaxServiceManager


class ProxyResource(Resource):
    @rate_limited(6)
    def get(self):
        args = self._ensure_args()
        self._ensure_valid_get_request(args.endpoint)

        service_manager = GdaxServiceManager(args.api_key, args.secret, args.passphrase)

        if args.request_type == 'GET':
            resp = service_manager.get(args.endpoint)
        elif args.request_type == 'POST':
            resp = service_manager.post(args.endpoint, args.data)
        elif args.request_type == 'PUT':
            resp = service_manager.put(args.endpoint, args.data)
        elif args.request_type == 'DELETE':
            resp = service_manager.delete(args.endpoint)
        else:
            resp = None

        return _data_to_response(resp)

    def options(self):
        # CORS...
        return _data_to_response(None)

    @staticmethod
    def _ensure_args():
        parser = reqparse.RequestParser()
        parser.add_argument('gdax-api-key', required=True, location='headers', dest='api_key')
        parser.add_argument('gdax-secret', required=True, location='headers', dest='secret')
        parser.add_argument('gdax-passphrase', required=True, location='headers', dest='passphrase')
        parser.add_argument('gdax-endpoint', required=True, location='headers', dest='endpoint')
        parser.add_argument('x-request-type', required=False, location='headers', dest='request_type')
        parser.add_argument('x-request-data', required=False, location='headers', dest='data')
        args = parser.parse_args()

        # Default is GET
        if not args.request_type:
            args.request_type = 'GET'

        args.request_type = args.request_type.strip().upper()

        if args.request_type not in ['GET', 'PUT', 'POST', 'DELETE']:
            abort(403, message="Forbidden request type provided: " + args.request_type)

        return args

    @staticmethod
    def _ensure_valid_get_request(endpoint):
        if not is_valid_get_endpoint(endpoint):
            abort(403, message='Forbidden endpoint for GET request')
