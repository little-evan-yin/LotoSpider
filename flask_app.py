from flask import Flask
import requests
from flask_cors import *


app = Flask(__name__)


def get_price():
    price_url = "http://www.lotoie.com/index.php/index/ajax?act=getShares"
    res = requests.get(price_url)
    data = res.json()
    print(data['data'])
    return res.json()


@app.route("/index")
@cross_origin(supports_credentials=True)
def hello_world():
    return get_price()


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
