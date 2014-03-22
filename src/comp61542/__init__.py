from flask import Flask

app = Flask(__name__)
app.debug = True

from comp61542 import views
