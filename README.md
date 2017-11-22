# GDAX Web Proxy

![GDAX: Trade digital currency](https://www.gdax.com/assets/gdax-card.d1bb192f4459bf2fa0aad1087b851bc1.jpg)

Due to GDAX restricting requests from other origins ([CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)), web developers do not have any ability to support embedding API calls into their pages. _This project resolves to alleviate that difficulty._

**For more information on the matter, see the Coinbase github discussion [here](https://github.com/coinbase/gdax-node/issues/116#issuecomment-332925708).**


This project enables developers to stand up their own GDAX proxy server internally and send/receive data from GDAX in the **same manner** as described in the [GDAX API Docs](https://docs.gdax.com/). Simply change the request pattern from `api.gdax.com/{resource}` to `{your_host}/{resource}`.

To use this project, ensure you have `python` and `pip` installed. Then, perform the following:

1. Install the required dependencies.
```
pip install -r requirements.txt
````

2. (OPTIONAL) Modify the `app\__init__.py` file and change your `host` and `port`.
```
app.run(host='0.0.0.0', port=3456, threaded=True)
```

3. Start the Flask server. You should see a `Running on...` message, if successful.
```
python app/__init__.py
```

## Using the proxy with your web app

Calling this proxy server is as simple as providing the `gdax-api-key`, `gdax-secret`, and `gdax-passphrase` as headers and the resource you want to request. The headers are [required to sign all requests using GDAX's authentication scheme](https://docs.gdax.com/#private). The proxy will do the work of generating the required `CB-ACCESS-*` headers and calling `api.gdax.com`.

For example, to call the [GET /accounts](https://docs.gdax.com/#accounts) resource on your local box, simply call the proxy as follows:
```
GET http://localhost:3456/accounts
{
    "gdax-api-key": "ABC",
    "gdax-secret": "DEF",
    "gdax-passphrase": "GHI"
}
```

Any responses from the GDAX API will be proxied back to your caller without CORS restrictions!

## TODO
* HTTPS support **(please don't use in a production setting without this)**