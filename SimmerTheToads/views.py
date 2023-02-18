"""Contains all the 'views' that the flask application itself uses."""
import functools
import json
import os

import spotipy
from flask import (Blueprint, Response, jsonify, redirect, render_template,
                   request, session, url_for)
from spotipy.oauth2 import SpotifyOAuth

# Retrieve these values from the spotify developer dashboard:
#   https://developer.spotify.com/dashboard/applications
#
# Set these in either .env or as environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# This needs to be set in your spotify dashboard!
REDIRECT_URI = "http://127.0.0.1:5000/api/login_callback"
OAUTH_SCOPES = [
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-private",
    "playlist-modify-public",
]
FRONTEND_URL = "http://127.0.0.1:3000"

# Setup the API blueprints
api_bp = Blueprint("api_bp", __name__)


def logged_in(func):
    """Ensure a user is logged in before using that endpoint.

    When used as a decarator, this function will automatically redirect to the
    login endpoint if there is no cached user login available. If there is a
    user logged in, the request is passed transparently to the function, along
    with an authenticated spotipy.Client.Spotify object.

    :param func: Function to guard against unauthenticate usage
    :returns: func

    Sample usage:

        @api_bp.route("/my-cool-endpoint")
        @logged_in
        def my_endpoint(spotify): # This parameter is required!
            . . .
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
        auth_manager = SpotifyOAuth(
            cache_handler=cache_handler,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
        )

        if not auth_manager.validate_token(cache_handler.get_cached_token()):
            # return redirect(url_for("api_bp.login"))
            return jsonify({"message": "Access denied"}), 401

        spotify = spotipy.Spotify(auth_manager=auth_manager)
        return func(*args, **kwargs, spotify=spotify)

    return wrapper


@api_bp.route("/")
def index():
    """Template response."""
    return jsonify({"message": "Hello from Flask!"})


@api_bp.route("/login", methods=["POST"])
def login():
    """Login to spotify's API using OAuth2.

    More documentation available here:
        * https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
        * https://github.com/spotipy-dev/spotipy/blob/master/examples/app.py
    """
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = SpotifyOAuth(
        scope=" ".join(OAUTH_SCOPES),
        cache_handler=cache_handler,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        show_dialog=True,
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1: Redirect to spotify OAuth when not logged in.
        auth_url = auth_manager.get_authorize_url()
        return jsonify({"auth_url": auth_url})

    return 500


@api_bp.route("/login_callback")
def login_callback():
    """Endpoint to receive token from Spotify's redirect."""
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = SpotifyOAuth(
        scope=" ".join(OAUTH_SCOPES),
        cache_handler=cache_handler,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        show_dialog=True,
    )
    if request.args.get("code"):
        # Step 2: Redirect from spotify back here.
        auth_manager.get_access_token(request.args.get("code"))
        return redirect(f"{FRONTEND_URL}/")

    return redirect(request.referrer or url_for("api_bp.login"))


@api_bp.route("/logout")
def logout():
    """Discard the token from the current session, logging out the user."""
    session.pop("token_info", None)
    return redirect("/")


@api_bp.route("/info")
@logged_in
def info(spotify):
    """Page describing information about the currently logged in user.

    :param spotify: Current spotify OAuth session
    """
    return render_template(
        "info.html",
        display_name=spotify.me()["display_name"],
    )


@api_bp.route("/playlists")
@logged_in
def playlists(spotify):
    """Get all the playlists of the current user.

    :param spotify: Current spotify OAuth session
    """
    return jsonify(spotify.current_user_playlists())


@api_bp.route("/get_test")
def get_test():
    """Demo get endpoint."""
    return jsonify({"key": "value", "ui": "perfect", "pages": 3})


@api_bp.route("/playlist", methods=["POST"])
def playlist():
    """Demo playlist post endpoint."""
    print(request.json)
    return jsonify(success=True)
