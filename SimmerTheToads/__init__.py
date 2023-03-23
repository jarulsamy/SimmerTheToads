"""Entrypoint to flask full-stack application."""

import secrets
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask_session import Session

LINE = "=" * 80


# Paths for production deployments
template_dir = Path("./frontend/build")
static_dir = template_dir / "static/"


print(LINE)
print(f"{template_dir.absolute()=}")
print(f"{static_dir.absolute()=}")

app = Flask(
    __name__,
    template_folder=str(template_dir.absolute()),
    static_folder=str(static_dir.absolute()),
)
app.config["SECRET_KEY"] = secrets.token_hex()
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["REMEMBER_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
cors_args = dict(supports_credentials=True)
Session(app)
CORS(app, **cors_args)


from .views import api_bp, frontend_bp

CORS(api_bp, **cors_args)

app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(frontend_bp, url_prefix="/")
