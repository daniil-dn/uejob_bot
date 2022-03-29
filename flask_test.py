import requests
from flask import *
from main import dp
from flask import abort, redirect, url_for
import aiogram
from requests import get

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_updates_from_webhook(path):
    print(path)
    return requests.post('https://localhost:8080/', data={})


if __name__ == '__main__':
  app.run(host='10.129.0.20', port=4400)