"""Contains all the 'views' that the flask application itself uses."""
import functools
import os

import spotipy
from flask import (Blueprint, jsonify, redirect, render_template, request,
                   session)
from spotipy.oauth2 import SpotifyOAuth

from .engine import ClusteringEvaluator, Playlist, batched, simmer_playlist
from .version import __version__

# Retrieve these values from the spotify developer dashboard:
#   https://developer.spotify.com/dashboard/applications
#
# Set these in either .env or as environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# This needs to be set in your spotify dashboard!
OAUTH_SCOPES = [
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-private",
    "playlist-modify-public",
]

# Setup the blueprints
frontend_bp = Blueprint("frontend_bp", __name__)
api_bp = Blueprint("api_bp", __name__)


@frontend_bp.route("/")
def frontend_index():
    """Return anything the frontend needs."""
    return render_template("index.html")


def logged_in(func):
    """Ensure a user is logged in before using that endpoint.

    When used as a decarator, this function will automatically reject requests
    with error 401 if there is no cached user login available. If there is a
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
            return jsonify({"message": "Access denied"}), 401

        spotify = spotipy.Spotify(auth_manager=auth_manager)
        return func(*args, **kwargs, spotify=spotify)

    return wrapper


@api_bp.route("/")
def api_index():
    """Template response."""
    return jsonify(
        {
            "version": __version__,
            "message": "Hello from Flask!",
        }
    )


@api_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login to spotify's API using OAuth2.

    Query whether logged in with GET.
    Login with POST.

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
    logged_in = (
        auth_manager.validate_token(cache_handler.get_cached_token()) is not None
    )

    if request.method == "GET":
        return jsonify({"logged_in": logged_in})
    elif request.method == "POST":
        if not logged_in:
            # Step 1: Redirect to spotify OAuth when not logged in.
            auth_url = auth_manager.get_authorize_url()
            return jsonify({"auth_url": auth_url})

    return jsonify(success=True)


@api_bp.get("/login_callback")
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
        # Close the popup oauth window.
        return "<script>if (window != top) window.close();</script>"

    # TODO: Make this prettier
    return "Something went wrong. Please try again.", 500


@api_bp.route("/logout")
def logout():
    """Discard the token from the current session, logging out the user."""
    session.pop("token_info", None)
    return redirect("/")


@api_bp.route("/playlists")
@logged_in
def playlists(spotify):
    """Get all the playlists of the current user."""
    playlists = spotify.current_user_playlists()
    my_id = spotify.me().get("id")

    # Filter to only those that the user owns
    items = playlists["items"]
    items = [i for i in items if i["owner"]["id"] == my_id]
    playlists["items"] = items

    return jsonify(playlists)


@api_bp.get("/playlist/<id>/tracks")
@logged_in
def get_playlist_tracks(spotify, id):
    """Get all the tracks of the currently selected playlist."""
    # Validate the playlist ID
    track_items = []
    result = spotify.user_playlist_tracks(playlist_id=id)
    track_items.extend(result["items"])
    while result["next"]:
        result = spotify.next(result)
        track_items.extend(result["items"])

    # Remove redundant information from responses
    track_items = [i["track"] for i in track_items]

    for i in track_items:
        del i["available_markets"]
        del i["album"]["available_markets"]

    return jsonify(track_items)


def ids_to_tracks(spotify, ids):
    """Convert a list of IDs to spotify track metadata."""
    result = []
    for batch in batched(ids, 50):
        result.extend(spotify.tracks(list(batch))["tracks"])

    for i, v in enumerate(result):
        del v["available_markets"]
        del v["album"]["available_markets"]
        v["index"] = i

    return result


@api_bp.get("/simmered_playlist/<id>/tracks")
@logged_in
def get_simmered_playlist(spotify, id):
    """Reorder a playlist and return the metadata."""
    # TODO: Parallel fetching doesn't currently work, child threads cannot use
    # the request context used by the token session management of Spotipy.
    # As a result, this is kinda slow...
    to_spotify = request.args.get("to_spotify", False)
    p = Playlist(spotify, id, parallel_fetch=False)

    tracks = simmer_playlist(p, ClusteringEvaluator, to_spotify=to_spotify)
    new_track_ids = [i.id for i in tracks]

    return jsonify(ids_to_tracks(spotify, new_track_ids))
