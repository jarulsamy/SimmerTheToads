from flask import render_template

from . import app


@app.route("/")
def index():
    """Demo root index."""
    return render_template("index.html")
