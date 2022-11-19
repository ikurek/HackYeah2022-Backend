from flask import Flask

from src.database import init_db

init_db()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'
