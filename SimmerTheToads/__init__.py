import os
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask_session import Session

line = "=" * 80

template_dir = os.getenv("STT_TEMPLATE_DIR")
if template_dir is None:
    template_dir = Path("../frontend/build")
    static_dir = template_dir / "static/"
else:
    template_dir = Path(template_dir)
    static_dir = template_dir.parent / "src/"


print(line)
print(f"{template_dir=}")
print(f"{static_dir=}")

app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir,
)
app.config["SECRET_KEY"] = os.urandom(64)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = False

Session(app)
CORS(app, supports_credentials=True)


from .views import api_bp

CORS(api_bp, support_credentials=True)

app.register_blueprint(api_bp, url_prefix="/api")

__version__ = "0.0.1"
