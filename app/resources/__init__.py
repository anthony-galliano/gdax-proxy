from flask import Response


def _data_to_response(data):
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Headers'] = ['gdax-api-key',
                                               'gdax-secret', 'gdax-passphrase', 'gdax-endpoint', 'x-request-data', 'x-request-type']

    try:
        return Response(data, mimetype='application/json', headers=headers, status=data.status_code)
    except AttributeError:
        return Response(data, mimetype='application/json', headers=headers)
