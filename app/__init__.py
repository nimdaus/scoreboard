from flask import Flask

app = Flask(__name__)
app.secret_key = '8f4cefa03edd963909d87244'

from app import views