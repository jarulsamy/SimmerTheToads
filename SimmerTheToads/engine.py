"""Primary playlist manipulation module."""
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Type

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from joblib import Parallel, delayed
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from sklearn.cluster import AgglomerativeClustering, KMeans, SpectralClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import (LabelEncoder, MinMaxScaler, RobustScaler,
                                   StandardScaler)
from spotipy.client import Spotify

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
plt.style.use("seaborn-v0_8-paper")


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

    analysis_df_names = (
        "bars",
        "beats",
        "sections",
        "segments",
        "tatums",
    )

    def __init__(self, spotify: Spotify, metadata: dict, features: dict):
        self._metadata = metadata
        self._features = features
        self._features["track"] = self
        self._spotify = spotify
        self._analysis = {}

        self._get_analysis()

    def _get_analysis(self):
        track_remove_keys = (
            "codestring",
            "code_version",
            "echoprintstring",
            "synchstring",
            "synch_version",
            "rythmstring",
            "rythm_version",
        )

        # TODO: This is somewhat slow since there are so many API calls.
        #       Maybe do this lazily/async?
        analysis = spotify.audio_analysis(self.id)

        # Remove unused track attributes
        for i in track_remove_keys:
            analysis["track"].pop(i, None)
        self._analysis["track"] = analysis["track"]

        for i in self.analysis_df_names:
            self._analysis[i] = pd.DataFrame(analysis[i])
            self._analysis[i] = self._analysis[i].query("confidence > 0.7")

    def plot(self):
        """Show plots based on Spotify's own analysis."""
        for i in self.analysis_df_names:
            self.analysis[i].plot(x="start")

        plt.show()

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
        """Get the audio analysis about this track.

        Data follows the following form.
        {
          meta: {...},
          track: {...},
          bars: pd.DataFrame(columns=["start", "duration", "confidence"]),
          beats: pd.DataFrame(columns=["start", "duration", "confidence"]),
          sections: pd.DataFrame(columns=["start",
                                          "duration",
                                          "confidence",
                                          "loudness",
                                          "tempo",
                                          "tempo_confidence",
                                          "key",
                                          "key_confidence",
                                          "mode",
                                          "mode_confidence",
                                          "time_signature",
                                          "time_signature_confidence"]),
          segments: pd.DataFrame(columns=["start",
                                          "duration",
                                          "confidence",
                                          "loudness_start",
                                          "loudness_max_time",
                                          "loudness_max",
                                          "loudness_end",
                                          "pitches",
                                          "timber"]),
          tatums: pd.DataFrame(columns=["start", "duration", "confidence"]),
        }
        """
        return self._analysis

    @property
    def num_bars(self):
        return len(self.analysis["bars"])

    @property
    def num_beats(self):
        return len(self.analysis["beats"])

    @property
    def num_sections(self):
        return len(self.analysis["sections"])

    @property
    def num_segments(self):
        return len(self.analysis["segments"])

    @property
    def num_tatums(self):
        return len(self.analysis["tatums"])

    def get_analysis_features(self, num_bars, num_beats, num_sections, num_tatums):
        base_features = self.features
        analysis = self.analysis

        # Add artist
        try:
            base_features["artist"] = self.metadata["artists"][0]["name"]
        except KeyError:
            base_features["artist"] = None

        rel_section_columns = [
            "start",
            "loudness",
            "tempo",
            "key",
            "mode",
            "time_signature",
        ]

        # Mean of groups of sections
        sections = analysis["sections"]
        sections = sections[rel_section_columns]
        sections = np.array_split(sections, num_sections)
        for i, v in enumerate(sections):
            for column in v.columns:
                base_features[f"section_{column}_{i}"] = v[column].mean()

        types = {
            "bars": num_bars,
            "beats": num_beats,
            "tatums": num_tatums,
        }
        for k, v in types.items():
            if v == 0:
                # Skip empty fields
                continue
            data = analysis[k]
            data = data[["start"]]
            splits = np.array_split(data, v)
            for i, split in enumerate(splits):
                for column in split.columns:
                    base_features[f"{k}_{column}_{i}"] = split[column].mean()

        return base_features

    def __repr__(self):
        name = self.metadata["name"][:16]
        artist = self.metadata["artists"][0]["name"][:16]
        return f"{name}, {artist}"


class Playlist:
    """Represent a Spotify playlist."""

    metadata: dict
    id: str
    name: Optional[str]
    df: pd.DataFrame
    _spotify: Spotify

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
        self._spotify = spotify
        self.metadata = self._spotify.playlist(id)

        # Retrieve all the tracks within the playlist
        # Handle the pagination
        track_items = []
        result = self._spotify.user_playlist_tracks(playlist_id=self.id)
        track_items.extend(result["items"])
        while result["next"]:
            result = self._spotify.next(result)
            track_items.extend(result["items"])

        track_ids = [i["track"]["id"] for i in track_items]

        # Get all the features of each track within the playlist.
        # Do this outside of the Track class to leverage the batched API.
        features = []
        for chunk in grouper(track_ids, min(len(track_ids), 100)):
            features.extend(self._spotify.audio_features(list(chunk)))

        results = Parallel(n_jobs=os.cpu_count(), prefer="threads")(
            delayed(Track)(self._spotify, m["track"], f)
            for m, f in zip(track_items, features)
        )

        analysis_params = {
            "num_bars": 0,
            "num_beats": 0,
            "num_sections": 0,
            "num_tatums": 0,
        }
        for i in analysis_params.keys():
            analysis_params[i] = getattr(
                min(results, key=lambda x: getattr(x, i)),
                i,
            )

        rows = [i.get_analysis_features(**analysis_params) for i in results]
        self.df = pd.DataFrame(rows)
        self.df = self.df.drop(
            labels=["type", "analysis_url"],
            axis=1,
            errors="ignore",
        )

        # Move track column to beginning for ease of reading output
        self.df.insert(0, "track", self.df.pop("track"))

    def to_disk(self, path: Path):
        """Dump the metadata to a JSON file on disk."""
        # Drop the track object reference
        serializeable_df = self.df.drop(["track"], axis=1)
        serializeable_df.to_json(path, orient="records", indent=4)

    def to_spotify(self):
        """Write the playlist back to spotify."""
        new_tracks = list(self.df["id"])
        self._spotify.playlist_replace_items(self.id, new_tracks)

    def reorder_by_feature(self, feature):
        """Reorder the playlist by a single feature."""
        self.df = self.df.sort_values(by=feature)
        self.df = self.df.reset_index()

    def corr_matrix(self, fmt_title=None) -> (Figure, Axes):
        """Generate a correlation matrix of the data features."""
        fig, ax = plt.subplots()
        matrix = self.df.corr(numeric_only=True)
        sns.heatmap(matrix, annot=True, ax=ax)

        if fmt_title is None:
            title = f"{self.metadata['name']}: Correlation Matrix"
        else:
            title = fmt_title.format(name=self.metadata["name"])
        ax.set_title(title)

        return fig, ax

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

        hue = "cluster_class_outer" if "cluster_class_outer" in self.df else None
        print(hue)
        for i, v in enumerate(relevant_cols):
            sns.lineplot(
                data=self.df,
                x=self.df.index,
                y=v,
                ax=lineplots_axes[i % (ncols + 1)][i // nrows],
                markers=True,
                hue=hue,
            )
            sns.histplot(
                data=self.df,
                x=v,
                ax=distplots_axes[i % (ncols + 1)][i // nrows],
                hue=hue,
            )

        if fmt_title is None:
            title = f"{self.metadata['name']}"
        else:
            title = fmt_title.format(name=self.metadata["name"])

        lineplots_fig.suptitle(title)
        lineplots_fig.tight_layout()

        distplots_fig.suptitle(title)
        distplots_fig.tight_layout()


class PlaylistEvaluatorBase(ABC):
    """Abstract base class for playlist raters."""

    @abstractmethod
    def __init__(self, playlist: Playlist):
        self._playlist = playlist

    @abstractmethod
    def reorder(self):
        """Reorder the songs within the existing playlist."""
        pass

    @abstractmethod
    def suggest(self):
        """Suggest songs to add in the playlist."""
        pass

    @property
    def playlist(self) -> Playlist:
        """Get the playlist being evaluated."""
        return self._playlist


class ClusteringEvaluator(PlaylistEvaluatorBase):
    """Evaluate playlists using sklearn's clustering algorithms."""

    def __init__(self, playlist: Playlist):
        super().__init__(playlist)

    def _preprocess_features(
        self,
        df: Optional[pd.DataFrame] = None,
    ) -> np.array:
        if df is None:
            df = self._playlist.df

        # Ordinal encode the artists
        le = LabelEncoder()
        artists = le.fit_transform(df["artist"])
        artists = np.atleast_2d(artists).T

        # Assume all numeric features are valid input features
        numeric_df = df.select_dtypes(include=[np.number])
        arr = numeric_df.to_numpy()
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(RobustScaler().fit_transform(arr))

        # Add artists column, exclude this from scaling
        scaled = np.append(scaled, artists, axis=1)

        # Principle component analysis
        pca = PCA(n_components=10)
        scaled = pca.fit_transform(scaled)
        print(f"{np.sum(pca.explained_variance_ratio_)=}")

        return scaled

    def reorder(self):
        """Reorder playlist using agglomerative clustering."""
        # Agglomerative
        features_matrix = self._preprocess_features()

        print(features_matrix)

        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=3,
        )
        labels = clustering.fit_predict(features_matrix)
        self._playlist.df["cluster_class_outer"] = labels
        self._playlist.df = self._playlist.df.sort_values(by=["cluster_class_outer"])

    def suggest(self):
        """Suggest songs to add in the playlist."""
        raise NotImplementedError


def simmer_playlist(
    p: Playlist,
    evaluator: Type[PlaylistEvaluatorBase],
    to_spotify: Optional[bool] = False,
) -> list[Track]:
    """Reorder / add songs to playlist for simmering.

    This is the main entrypoint to the playlist processing engine. It queries a
    playlist for all the required information about a playlist, then reorders
    the playlist. This aims to be an abstraction to avoid requiring the Spotify
    API to be passed deep into the engine.

    TODO: Reword this with new 'Evaluator' model.

    :param spotify: Current spotify OAuth session
    :param playlist_id: ID of the playlist to simmer.

    """
    # p.corr_matrix()
    # p.plot(fmt_title="{name}: Original")

    e = evaluator(p)
    e.reorder()

    # p.plot(
    #     fmt_title="{{name}}: Reordered by {feature}".format(
    #         feature=evaluator.__name__,
    #     )
    # )
    print(p.df[["track", "cluster_class_outer"]])

    # Propogate local changes back to spotify playlist
    if to_spotify:
        p.to_spotify()

    # reorder_feature = "liveness"
    # p.reorder_by_feature(reorder_feature)
    # p.plot(fmt_title="{{name}}: Reordered by {feature}".format(feature=reorder_feature))

    plt.show()


if __name__ == "__main__":
    # For the sake of testing without spinning up the entire web application.
    import spotipy
    from dotenv import load_dotenv
    from spotipy.oauth2 import SpotifyOAuth

    load_dotenv()

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = "http://127.0.0.1:5000/api/login_callback"
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
        "close but no cigar copy": "5jrJfrjQsK1H4ebNdPvafK",
        "manic pixie dream girl complex": "3ZL5feDBYxJSWR6zg7EDeu",
        "kotlin": "5IrrDF6L9eiXjIAS6qTx5E",
        "mainstream": "0Or7sOLeS5ikhhOaWWRyzC",
        "girls party!": "2ZleY8ep3CsifUlv8rECfG",
        "4 cat copy": "3r4jK8owZWGUe8ET3YqPFG",
    }

    cache_path = Path("./playlist.pickle")
    p = Playlist(spotify, playlists["mainstream"])
    # if cache_path.is_file():
    #     with open(cache_path, "rb") as f:
    #         p = pickle.load(f)
    # else:
    #     p = Playlist(spotify, playlists["girls party!"])
    #     with open(cache_path, "wb") as f:
    #         pickle.dump(p, f)

    simmer_playlist(
        p,
        ClusteringEvaluator,
        to_spotify=True,
    )
