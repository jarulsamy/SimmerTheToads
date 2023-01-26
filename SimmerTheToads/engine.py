"""Primary playlist manipulation module."""
import os
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from spotipy.client import Spotify

# pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


def grouper(iterable, n):
    """Collect data into non-overlapping fixed-length chunks or blocks.

    Adapted from the more-itertools recipes section:
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    args = [iter(iterable)] * n
    return zip(*args)


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

    metadata: dict
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

    def __init__(self, spotify: Spotify, id: str):
        self.id = id
        self.metadata = spotify.playlist(id)

        # Retrieve all the tracks within the playlist
        # Handle the pagination
        track_items = []
        result = spotify.user_playlist_tracks(playlist_id=self.id)
        track_items.extend(result["items"])
        while result["next"]:
            result = spotify.next(result)
            track_items.extend(result["items"])

        track_ids = [i["track"]["id"] for i in track_items]

        # Get all the features of each track within the playlist.
        # Do this outside of the Track class to leverage the batched API.
        features = []
        for chunk in grouper(track_ids, 100):
            features.extend(spotify.audio_features(list(chunk)))

        rows = []
        for metadata, features in zip(track_items, features):
            t = Track(spotify, metadata["track"], features)
            rows.append(t.features)

        self.df = pd.DataFrame(rows, columns=self.FEATURE_COLUMNS)

    def to_disk(self, path: Path):
        """Dump the metadata to a JSON file on disk."""
        # Drop the track object reference
        serializeable_df = self.df.drop(["track"], axis=1)
        serializeable_df.to_json(path, orient="records", indent=4)

    def reorder_by_feature(self, feature):
        """Reorder the playlist by a single feature."""
        self.df = self.df.sort_values(by=feature)
        self.df = self.df.reset_index()

    def plot(self, fmt_title=None):
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
            sns.lineplot(
                data=self.df,
                x=self.df.index,
                y=v,
                ax=lineplots_axes[i % (ncols + 1)][i // nrows],
                markers=True,
            )
            sns.histplot(
                data=self.df,
                x=v,
                ax=distplots_axes[i % (ncols + 1)][i // nrows],
            )

        if fmt_title is None:
            title = f"{self.metadata['name']}"
        else:
            title = fmt_title.format(name=self.metadata["name"])

        lineplots_fig.suptitle(title)
        lineplots_fig.tight_layout()

        distplots_fig.suptitle(title)
        distplots_fig.tight_layout()


def simmer_playlist(
    spotify: Spotify,
    playlist_id: str,
) -> list[Track]:
    """Reorder / add songs to playlist for simmering.

    This is the main entrypoint to the playlist processing engine. It queries a
    playlist for all the required information about a playlist, then reorders
    the playlist. This aims to be an abstraction to avoid requiring the Spotify
    API to be passed deep into the engine.

    :param spotify: Current spotify OAuth session
    :param playlist_id: ID of the playlist to simmer.

    """
    p = Playlist(spotify, playlist_id)
    p.to_disk(Path("playlist.json"))
    p.plot(fmt_title="{name}: Original")

    reorder_feature = "acousticness"
    p.reorder_by_feature(reorder_feature)

    p.plot(fmt_title="{{name}}: Reordered by {feature}".format(feature=reorder_feature))

    plt.show()


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

    # Just an easy way to quickly switch between playlists for testing.
    playlists = {
        "Abbey Road": "2CPPiUTAtfvaeAEyWApOSE",
        "Fiddler on the roof": "3engsNaAr6Q9cTT85gKCGd",
        "Josh's Jar of Samys": "3Wh0AUvdYEg6fz0zmpwaH6",
        "Lona and Josh's Code Think Tank": "0GJIoDOUsoSS2IDWniCTqP",
        "The Big Bach": "4OFbt8ZZOhE0oZcC4GGBMO",
        "godawful amalgamation": "0KOMGaR3mgeymmUBoN0ZlQ",
        "close but no cigar": "78C62xSuql1V2jwMvonI4N",
        "manic pixie dream girl complex": "3ZL5feDBYxJSWR6zg7EDeu",
    }
    simmer_playlist(spotify, playlists["The Big Bach"])
