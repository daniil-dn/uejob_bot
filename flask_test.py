import flask
from flask import Flask
from flask import abort, redirect, url_for

app = Flask(__name__)


@app.route('/<data>', methods=['GET', 'POST'])
def index(data):
    print(data)

    return redirect(url_for(f'localhost:4443/{flask.request.data}'))



if __name__ == '__main__':
    app.run()
