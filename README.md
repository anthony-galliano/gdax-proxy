# GDAX Web Proxy

![GDAX: Trade digital currency](https://www.gdax.com/assets/gdax-card.d1bb192f4459bf2fa0aad1087b851bc1.jpg)

Due to GDAX restricting requests from other origins ([CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)), web developers do not have any ability to support embedding API calls into their pages. _This project resolves to alleviate that difficulty._

**For more information on the matter, see the Coinbase github discussion [here](https://github.com/coinbase/gdax-node/issues/116#issuecomment-332925708).**


This project enables developers to stand up their own GDAX proxy server internally and receive data from GDAX matching the schema those described in the [GDAX API Docs](https://docs.gdax.com/).

To use this project, ensure you have `python` and `pip` installed. Then, perform the following:

1. Install the required dependencies.
```
pip install -r requirements.txt
````

2. Modify the `app\__init__.py` file and change your `host` and `port` as applicable.
```
app.run(host='0.0.0.0', port=3456, threaded=True)
```

3. Start the Flask server. You should see a `Running on...` message, if successful.
```
python app/__init__.py
```

Calling this proxy server is as simple as providing your `api_key`, `secret`, and `passphrase` (as required in the GDAX API Docs) and the `endpoint` you wish to call. Additionally, you may ned to supply `x-request-type` and `x-request-data` if you're proxying a `POST` or `PUT` API on GDAX.

For example, to call the [GET /accounts](https://docs.gdax.com/#accounts) endpoint simply call the proxy as follows (if using the default host/port):
```
GET http://localhost:3456/api/proxy
{
    "gdax-api-key": "ABC",
    "gdax-secret": "DEF",
    "gdax-passphrase": "GHI",
    "gdax-endpoint": "/accounts"
    "x-request-type": "GET" (default is GET and can be omitted)
    "x-request-data": { ... } (this is only relevant for POST and PUT requests)
}
```

_That is, in general, the only thing that'll change about your request to the proxy is the `gdax-endpoint` header value.

Any responses from GDAX will be proxied to your caller without CORS restrictions!

## TODO: 
* HTTPS support **(please don't use in a production setting without this)**