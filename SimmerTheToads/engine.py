"""Primary playlist manipulation module."""
import itertools
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Type

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import scipy
import seaborn as sns
from joblib import Parallel, delayed
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, RobustScaler
from spotipy.client import Spotify

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
np.set_printoptions(suppress=True)
plt.style.use("seaborn-v0_8-paper")


def grouper(iterable, n):
    """Collect data into non-overlapping fixed-length chunks or blocks.

    Adapted from the more-itertools recipes section:
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    args = [iter(iterable)] * n
    return zip(*args)


def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


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

    def _get_analysis(self) -> None:
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
        analysis = self._spotify.audio_analysis(self.id)

        # Remove unused track attributes
        for i in track_remove_keys:
            analysis["track"].pop(i, None)
        self._analysis["track"] = analysis["track"]

        for i in self.analysis_df_names:
            self._analysis[i] = pd.DataFrame(analysis[i])
            self._analysis[i] = self._analysis[i].query("confidence > 0.7")

    def plot(self) -> None:
        """Show plots based on Spotify's own analysis."""
        for i in self.analysis_df_names:
            self.analysis[i].plot(x="start")

        plt.show()

    @property
    def id(self) -> str:
        """Get the Spotify ID of this track."""
        return self._metadata["id"]

    @property
    def metadata(self) -> dict:
        """Get the raw metadata about this track."""
        return self._metadata

    @property
    def features(self) -> dict:
        """Get the audio features about this track."""
        return self._features

    @property
    def analysis(self) -> dict:
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
    def num_bars(self) -> int:
        """Get the number of bars."""
        return len(self.analysis["bars"])

    @property
    def num_beats(self) -> int:
        """Get the number of beats."""
        return len(self.analysis["beats"])

    @property
    def num_sections(self) -> int:
        """Get the number of sections."""
        return len(self.analysis["sections"])

    @property
    def num_segments(self) -> int:
        """Get the number of segments."""
        return len(self.analysis["segments"])

    @property
    def num_tatums(self) -> int:
        """Get the number of tatums."""
        return len(self.analysis["tatums"])

    def get_analysis_features(
        self, num_bars, num_beats, num_sections, num_tatums
    ) -> dict:
        """TODO."""
        base_features = self.features
        analysis = self.analysis

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

    def __repr__(self) -> str:
        """Represent a track as 'name', 'artist'."""
        name = self.metadata["name"]
        artist = self.metadata["artists"][0]["name"]
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

    def __init__(self, spotify: Spotify, id: str, parallel_fetch=True):
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
        for chunk in batched(track_ids, min(len(track_ids), 100)):
            features.extend(self._spotify.audio_features(list(chunk)))

        if parallel_fetch:
            results = Parallel(n_jobs=os.cpu_count(), prefer="threads")(
                delayed(Track)(self._spotify, m["track"], f)
                for m, f in zip(track_items, features)
            )
        else:
            results = [
                Track(self._spotify, m["track"], f)
                for m, f in zip(track_items, features)
            ]
        if not results:
            raise ValueError("Cannot construt empty playlist")

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
        scale: bool = True,
    ) -> np.array:
        if df is None:
            df = self._playlist.df

        # Ordinal encode the artists
        if not np.issubdtype(df["artist"].dtype, np.number):
            le = LabelEncoder()
            artist = le.fit_transform(df["artist"])
            artist = np.atleast_2d(artist).T
            df["artist"] = artist

        # Assume all numeric features are valid input features
        numeric_df = df.select_dtypes(include=[np.number])
        if not scale:
            return numeric_df.to_numpy()

        r_scaler = RobustScaler()
        mm_scaler = MinMaxScaler()

        # Exclude categorical features from scaling
        artist = numeric_df["artist"]
        numeric_df = numeric_df.drop(labels=["artist"], axis=1)
        # TODO: Investigate the deprecation warning
        numeric_df[:] = r_scaler.fit_transform(numeric_df)
        numeric_df[:] = mm_scaler.fit_transform(numeric_df)
        numeric_df["artist"] = artist
        scaled = numeric_df.to_numpy()

        # Principle component analysis
        try:
            pca = PCA(n_components=10)
            scaled = pca.fit_transform(scaled)
        except ValueError:
            # Very few tracks or features.
            pca = PCA(n_components=min(*numeric_df.shape))
            scaled = pca.fit_transform(scaled)

        return scaled

    def _cluster(self):
        """Reorder playlist using agglomerative clustering."""
        feature_matrix = self._preprocess_features()
        if len(feature_matrix) <= 1:
            labels = list(range(len(feature_matrix)))
        else:
            clustering = AgglomerativeClustering(
                n_clusters=None,
                distance_threshold=3,
                linkage="ward",
            )
            labels = clustering.fit_predict(feature_matrix)

        self._playlist.df["cluster_class_outer"] = labels
        self._playlist.df = self._playlist.df.sort_values(
            by=["cluster_class_outer"],
        )

    def _subcluster_opt(self):
        self._playlist.df["cluster_class_inner"] = 0
        for cluster in self._playlist.df["cluster_class_outer"].unique():
            df = self._playlist.df.query("cluster_class_outer == @cluster")
            if len(df) <= 1:
                # Can't optimize a single song cluster
                continue

            # Compute euclidean distance of all the features within the matrix
            # TODO: Artist will definitely be wrong during this calculation...
            feature_matrix = df.select_dtypes(include=[np.number])
            feature_matrix = feature_matrix.drop(
                labels=["cluster_class_outer", "cluster_class_inner"],
                axis=1,
                errors="ignore",
            )
            feature_matrix = feature_matrix.to_numpy()
            distance_matrix = scipy.spatial.distance_matrix(
                feature_matrix, feature_matrix
            )

            # Convert to int for some possible speedup. These numbers are always
            # very large, so any rounding error is basically irrelevant.
            distance_matrix = distance_matrix.astype(int)

            if np.sum(distance_matrix) == 0:
                # Cluster of all the same songs, give them all the same inner class
                self._playlist.df.loc[
                    self._playlist.df.eval("cluster_class_outer == @cluster"),
                    "cluster_class_inner",
                ] = 0
                continue

            G = nx.from_numpy_array(distance_matrix)
            tsp = nx.approximation.traveling_salesman_problem
            path = tsp(G, cycle=False)

            self._playlist.df.loc[
                self._playlist.df.eval("cluster_class_outer == @cluster"),
                "cluster_class_inner",
            ] = path

        self._playlist.df["cluster_class_inner"] = self._playlist.df[
            "cluster_class_inner"
        ].astype(int)
        self._playlist.df = self._playlist.df.sort_values(
            by=["cluster_class_outer", "cluster_class_inner"]
        )

    def _order_clusters(self):
        """Reorder the clusters to minimize TSP across them."""
        clusters = self._playlist.df["cluster_class_outer"].unique()
        n_clusters = len(clusters)
        if n_clusters <= 1:
            return

        distance_matrix = np.zeros((n_clusters, n_clusters))

        df = self._playlist.df.select_dtypes(include=[np.number])
        for i, src in enumerate(clusters):
            src_df = df.query("cluster_class_outer == @src")
            src_df = src_df.set_index("cluster_class_inner")
            # Last node from every cluster connects to first node within every
            # other node.
            src_node = src_df.iloc[-1]
            src_node = src_node.drop(
                labels=["cluster_class_outer", "cluster_class_inner"],
                errors="ignore",
            )
            src_node = np.atleast_2d(src_node.to_numpy())
            for j, dst in enumerate(clusters):
                dst_df = df.query("cluster_class_outer == @dst")
                dst_df = dst_df.set_index("cluster_class_inner")
                dst_node = dst_df.iloc[0]
                dst_node = dst_node.drop(
                    labels=["cluster_class_outer", "cluster_class_inner"],
                    errors="ignore",
                )
                dst_node = np.atleast_2d(dst_node.to_numpy())
                distance = scipy.spatial.distance.cdist(src_node, dst_node)
                distance_matrix[i, j] = distance

        G = nx.from_numpy_array(distance_matrix)
        tsp = nx.approximation.traveling_salesman_problem
        path = tsp(G, cycle=False)
        # Ensure the path contains no duplicates, but also preserve the order.
        # TODO: This could indicate a TSP bug...
        path = list(dict.fromkeys(path))

        # Generate the new resulting dataframe
        # TODO: There may be a more performant way to do this.
        result = pd.DataFrame()
        for i in path:
            result = pd.concat(
                [result, self._playlist.df.query("cluster_class_outer == @i")]
            )

        self._playlist.df = result

    def reorder(self):
        """Reorder playlist combining several techniques."""
        self._cluster()
        self._subcluster_opt()
        self._order_clusters()

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
    the playlist based on the evaluation of 'evaluator'.

    :param p: Playlist to be reordered.
    :param evaluator: Engine to use for the evaluation.
    :param to_spotify: Whether to write the modified playlist back to spotify.
    """
    e = evaluator(p)
    e.reorder()
    # e.suggest()

    print(p.df[["track", "cluster_class_outer", "cluster_class_inner"]])

    # Propogate local changes back to spotify playlist
    if to_spotify:
        p.to_spotify()

    return list(p.df["track"])


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
        "4 songs": "4C9aR5IxztGLZNWQrdO8Y1",
        "Bring it on back": "6HBoSjDYkQ5EKufcCbGja1",
    }

    cache_path = Path("./playlist.pickle")
    p = Playlist(spotify, playlists["Bring it on back"])

    simmer_playlist(
        p,
        ClusteringEvaluator,
        to_spotify=True,
    )
