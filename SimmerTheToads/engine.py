"""TODO."""
import os
from pprint import pprint
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from spotipy.client import Spotify

# pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


class Track:
    """Represent a single Spotify track."""

    _metadata: dict
    _features: dict
    _analysis: dict
    _spotify: Spotify

    def __init__(self, spotify: Spotify, metadata: dict, features: dict):
        self._metadata = metadata
        self._features = features
        self._features["track"] = self
        self._spotify = spotify

        self._get_analysis()

    def _get_analysis(self):
        self._analysis = {}
        # TODO: This is really slow since there are so many API calls.
        #       Maybe do this lazily?
        # self._analysis = spotify.audio_analysis(self.id)

    @property
    def id(self):
        """Get the Spotify ID of this track."""
        return self._metadata["id"]

    @property
    def metadata(self):
        """Get the raw metadata about this track."""
        return self._metadata

    @property
    def features(self):
        """Get the audio features about this track."""
        return self._features

    @property
    def analysis(self):
        """Get the audio analysis about this track."""
        return self._analysis


class Playlist:
    """Represent a Spotify playlist."""

    id: str
    name: Optional[str]
    df: pd.DataFrame

    FEATURE_COLUMNS = [
        "id",
        "acousticness",
        "analysis_url",
        "danceability",
        "duration_ms",
        "energy",
        "instrumentalness",
        "key",
        "liveness",
        "loudness",
        "mode",
        "speechiness",
        "tempo",
        "time_signature",
        "track_href",
        "valence",
        "track",
    ]

    def __init__(self, spotify, id, name=None):
        self.id = id
        self.name = name

        # Retrieve all the tracks within the playlist
        track_data = spotify.user_playlist_tracks(playlist_id=self.id)
        track_ids = [i["track"]["id"] for i in track_data["items"]]

        # Get all the features of each track within the playlist.
        # Do this outside of the Track class to leverage the batched API.
        features = spotify.audio_features(track_ids)

        rows = []
        for metadata, features in zip(track_data["items"], features):
            t = Track(spotify, metadata["track"], features)
            rows.append(t.features)

        self.df = pd.DataFrame(rows, columns=self.FEATURE_COLUMNS)

    def plot(self):
        """Show some simple statistics about this playlist."""
        nrows = 4
        ncols = 3
        lineplots_fig, lineplots_axes = plt.subplots(
            nrows=nrows, ncols=ncols, figsize=(16, 12)
        )
        distplots_fig, distplots_axes = plt.subplots(
            nrows=nrows, ncols=ncols, figsize=(16, 12)
        )
        relevant_cols = [
            "acousticness",
            "danceability",
            "duration_ms",
            "energy",
            "instrumentalness",
            "key",
            "liveness",
            "loudness",
            "mode",
            "speechiness",
            "tempo",
            "time_signature",
        ]

        for i, v in enumerate(relevant_cols):
            ax = lineplots_axes[i % (ncols + 1)][i // nrows]
            sns.lineplot(data=self.df, x=self.df.index, y=v, ax=ax)

        for i, v in enumerate(relevant_cols):
            ax = distplots_axes[i % (ncols + 1)][i // nrows]
            sns.histplot(
                data=self.df,
                x=v,
                ax=ax,
            )

        lineplots_fig.suptitle(f"{self.name}")
        lineplots_fig.tight_layout()

        distplots_fig.suptitle(f"{self.name}")
        distplots_fig.tight_layout()
        plt.show()


def simmer_playlist(
    spotify: Spotify,
    playlist_id: str,
    playlist_name: Optional[str] = None,
) -> list[Track]:
    """
    Reorder / add songs to playlist for simmering.

    This is the main entrypoint to the playlist processing engine. It queries a
    playlist for all the required information about a playlist, then reorders
    the playlist. This aims to be an abstraction to avoid requiring the Spotify
    API to be passed deep into the engine.

    :param spotify: Current spotify OAuth session
    :param playlist_id: ID of the playlist to simmer.
    """
    # TODO: This will need to handle the pagination eventually
    #       Currently, this will only handle the first 100 songs.
    #       Also, beware the rate limit...
    p = Playlist(spotify, playlist_id, playlist_name)
    p.plot()


if __name__ == "__main__":
    # For the sake of testing without spinning up the entire web application.
    import spotipy
    from dotenv import load_dotenv
    from spotipy.oauth2 import SpotifyOAuth

    load_dotenv()

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = "http://localhost:5000/login_callback"
    OAUTH_SCOPES = [
        "playlist-read-private",
        "playlist-read-collaborative",
        "playlist-modify-private",
        "playlist-modify-public",
    ]

    auth_manager = SpotifyOAuth(
        scope=" ".join(OAUTH_SCOPES),
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        show_dialog=True,
    )

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    playlist_name = "Josh's Jar of Samys"
    playlist_id = "3Wh0AUvdYEg6fz0zmpwaH6"
    simmer_playlist(spotify, playlist_id, playlist_name)
