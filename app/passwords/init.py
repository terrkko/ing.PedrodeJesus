from flask import Flask

app = Flask(__name__)
app.secret_key = '1234'

from app import routes

