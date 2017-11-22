from flask import Flask
from flask_restful import Api

from routes import setup

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    setup(api)
    app.run(host='0.0.0.0', port=3456, threaded=True)
