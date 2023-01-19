from flask import Flask

app = Flask(__name__)

from .views import index

__version__ = "0.0.1"
