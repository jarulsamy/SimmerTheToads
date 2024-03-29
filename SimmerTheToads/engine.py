"""Primary playlist manipulation module."""
import heapq
import itertools
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Type

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

logger = logging.getLogger("SimmerTheToads")

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
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


def pairwise(iterable):
    """Return sliding pairs from an iterable.

    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


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

    def __init__(
        self,
        spotify: Spotify,
        metadata: dict,
        features: dict,
        get_analysis=True,
    ):
        self._metadata = metadata
        self._features = features
        self._features["track"] = self
        self._spotify = spotify
        self._analysis = {}

        if get_analysis:
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
        self,
        num_bars: int,
        num_beats: int,
        num_sections: int,
        num_tatums: int,
    ) -> dict:
        """Get a Dataframe of all features used for analysis/clustering."""
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
            # TODO: Repair this for flask requests.
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

        for i, v in enumerate(relevant_cols):
            sns.lineplot(
                data=self.df,
                x=self.df.index,
                y=v,
                ax=lineplots_axes[i % (ncols + 1)][i // nrows],
                markers=True,
                hue=None,
            )
            sns.histplot(
                data=self.df,
                x=v,
                ax=distplots_axes[i % (ncols + 1)][i // nrows],
                hue=None,
            )

        if fmt_title is None:
            title = f"{self.metadata['name']}"
        else:
            title = fmt_title.format(name=self.metadata["name"])

        lineplots_fig.suptitle(title)
        lineplots_fig.tight_layout()

        distplots_fig.suptitle(title)
        distplots_fig.tight_layout()

    def __len__(self):
        """Get the number of tracks within this playlist."""
        return len(self.df)


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
        df = self._playlist.df
        sort_cols = [i for i in df.columns if i.startswith("sort_")]
        largest_sort_col = max(sort_cols, key=lambda x: int(x.split("_")[1]))
        largest_sort_col = int(largest_sort_col.split("_")[1])
        my_sort_col = f"sort_{largest_sort_col + 1}"
        df[my_sort_col] = 0

        # TODO: Handle single song playlist

        # Preprocess
        # Up to 1/4 of the songs in the final playlist can be suggestions.
        max_suggestions = len(df) // 4
        rows = list(df.iterrows())
        cols_to_remove = [
            "track",
            "artist",
            "id",
            "uri",
            "track_href",
        ]

        # Determine where we need to suggest new songs.
        #
        # Slide along the playlist in pairs ((a[0], a[1]), (a[1], a[2]), etc.),
        # and find the two songs with the greatest distance.
        distances = {}
        for (i, first), (j, second) in pairwise(rows):
            first = first.drop(cols_to_remove).to_numpy()
            second = second.drop(cols_to_remove).to_numpy()
            dist = scipy.spatial.distance.hamming(first, second)
            distances[(i, j)] = dist

        suggestion_locs = heapq.nlargest(
            max_suggestions,
            distances,
            key=distances.get,
        )

        # These are all supported by Spotify's recommendation API as targets.
        feature_cols = [
            "acousticness",
            "danceability",
            "energy",
            "instrumentalness",
            "liveness",
            "loudness",
            "speechiness",
            "valence",
        ]
        # Get the actual suggestions and their locations
        for i, j in suggestion_locs:
            first = df.iloc[i]
            second = df.iloc[j]

            first_id = first.id
            second_id = second.id

            first_features = first[feature_cols]
            second_features = second[feature_cols]
            avg = (first_features + second_features) / 2

            # Assemble the payload for the Spotify API
            args = {"seed_tracks": [first_id, second_id], "limit": 3}
            for col in feature_cols:
                args[f"target_{col}"] = avg[col]

            # Retrieve suggestions from Spotify
            suggestions = self._playlist._spotify.recommendations(**args)
            track_ids = [i["id"] for i in suggestions.get("tracks", [])]

            # Preprocess all the incoming data
            features = []
            for b in batched(track_ids, min(len(track_ids), 100)):
                features.extend(self._playlist._spotify.audio_features(list(b)))

            tracks = []
            for m, f in zip(suggestions.get("tracks", []), features):
                t = Track(self._playlist._spotify, m, f, get_analysis=False)
                tracks.append(t)

            rows = [i.features for i in tracks]
            suggestion_df = pd.DataFrame(rows)
            suggestion_df = suggestion_df.drop(
                labels=["type", "analysis_url"],
                axis=1,
                errors="ignore",
            )
            suggestion_df.index = range(1, len(suggestion_df) + 1, 1)

            # Find the song with the smallest distance from first and second
            #
            # Essentially, add the existing first and second songs as the first
            # and last songs within the list of suggestions. Then, compute a
            # fully-connected graph of the distances (like before). Remove the
            # edge from the first and last tracks to force computation of a path
            # including a suggested song.
            suggestion_features = suggestion_df[feature_cols].copy()

            first_index = 0
            second_index = len(suggestion_df)

            suggestion_features.loc[first_index] = first_features.values
            suggestion_features.loc[second_index] = second_features.values
            suggestion_features = suggestion_features.sort_index()
            suggestion_arr = suggestion_features.to_numpy()

            distance_matrix = scipy.spatial.distance_matrix(
                suggestion_arr, suggestion_arr
            )
            G = nx.from_numpy_array(distance_matrix)
            G.remove_edge(first_index, second_index)
            _, suggestion_index, _ = nx.algorithms.shortest_path(
                G, source=first_index, target=second_index
            )
            ins_key = len(df)
            df.loc[ins_key] = suggestion_df.loc[suggestion_index]
            # Copy all the positional information of the song track before me.
            df.loc[ins_key, sort_cols] = df.loc[i, sort_cols]
            df.loc[ins_key, my_sort_col] = suggestion_index
            df.fillna(0, inplace=True)

    @property
    def playlist(self) -> Playlist:
        """Get the playlist being evaluated."""
        return self._playlist


class TSPEvaluator(PlaylistEvaluatorBase):
    """Evaluate playlists only using TSP.

    Compute a feature matrix from all the songs within the playlist. Minimize
    the distance of a tour through the playlist by reordering the tracks.
    Distance can be computed with a variety of functions; euclidean, hamming,
    etc.
    """

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
        artist = le.fit_transform(df["artist"])
        artist = np.atleast_2d(artist).T
        df["artist_ord"] = artist

        # Assume all numeric features are valid input features
        numeric_df = df.select_dtypes(include=[np.number])

        mm_scaler = MinMaxScaler()
        numeric_df[:] = mm_scaler.fit_transform(numeric_df)
        scaled = numeric_df.to_numpy()

        return scaled

    def reorder(self):
        """Reorder the songs within the existing playlist."""
        feature_matrix = self._preprocess_features()
        distance_matrix = scipy.spatial.distance_matrix(
            feature_matrix,
            feature_matrix,
        )

        G = nx.from_numpy_array(distance_matrix)
        path = nx.approximation.traveling_salesman_problem(
            G,
            weight="weight",
            nodes=set(G.nodes),
            cycle=False,
        )
        if len(path) != len(distance_matrix):
            logger.warning(
                "Path length does not match distance matrix size (%d != %d)",
                len(path),
                len(distance_matrix),
            )
            path = list(dict.fromkeys(path))

        self._playlist.df["sort_1"] = path

    def suggest(self):
        """Suggest songs to add in the playlist."""
        return super().suggest()


class ClusteringEvaluator(PlaylistEvaluatorBase):
    """Evaluate playlists using sklearn's clustering algorithms.

    Compute a feature matrix from all the songs within the playlist. Attempt to
    find clusters within the tracks, then reorder those clusters (and tracks) by
    minimizing the distance of TSP tour through the playlist.
    """

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
        le = LabelEncoder()
        artist = le.fit_transform(df["artist"])
        artist = np.atleast_2d(artist).T
        df["artist_ord"] = artist

        # Assume all numeric features are valid input features
        numeric_df = df.select_dtypes(include=[np.number])
        if not scale:
            return numeric_df.to_numpy()

        r_scaler = RobustScaler()
        mm_scaler = MinMaxScaler()

        # Exclude categorical features from scaling
        artist = numeric_df["artist_ord"]
        numeric_df = numeric_df.drop(labels=["artist_ord"], axis=1)
        # TODO: Investigate the deprecation warning
        numeric_df[:] = r_scaler.fit_transform(numeric_df)
        numeric_df[:] = mm_scaler.fit_transform(numeric_df)
        numeric_df["artist_ord"] = artist
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
        self._playlist.df["sort_1"] = labels
        logger.info(
            "Playlist: %s with %d songs has %d clusters",
            self._playlist.id,
            len(self._playlist),
            len(set(labels)),
        )

    def _subcluster_opt(self):
        self._playlist.df["sort_2"] = 0
        for cluster in self._playlist.df["sort_1"].unique():
            df = self._playlist.df.query("sort_1 == @cluster")
            if len(df) <= 1:
                # Can't optimize a single song cluster
                continue

            # Compute distance of all the features within the matrix
            feature_matrix = df.select_dtypes(include=[np.number])
            to_drop = [i for i in feature_matrix.columns if i.startswith("sort_")]
            feature_matrix = feature_matrix.drop(
                labels=to_drop,
                axis=1,
                errors="ignore",
            )
            feature_matrix = feature_matrix.to_numpy()
            distance_matrix = scipy.spatial.distance_matrix(
                feature_matrix, feature_matrix
            )

            if np.sum(distance_matrix) == 0:
                # Cluster of all the same songs
                continue

            G = nx.from_numpy_array(distance_matrix)
            path = nx.approximation.traveling_salesman_problem(G, cycle=False)
            if len(path) != len(distance_matrix):
                logger.warning(
                    "Path length does not match distance matrix size (%d != %d)",
                    len(path),
                    len(distance_matrix),
                )
                path = list(dict.fromkeys(path))

            self._playlist.df.loc[
                self._playlist.df.eval("sort_1 == @cluster"),
                "sort_2",
            ] = path

    def _order_clusters(self):
        """Reorder the clusters to minimize TSP across them."""
        clusters = self._playlist.df["sort_1"].unique()
        n_clusters = len(clusters)
        if n_clusters <= 1:
            return

        distance_matrix = np.zeros((n_clusters, n_clusters))

        df = self._playlist.df.select_dtypes(include=[np.number])
        for i, src in enumerate(clusters):
            src_df = df.query("sort_1 == @src")
            src_df = src_df.set_index("sort_2")
            # Last node from every cluster connects to first node within every
            # other node.
            src_node = src_df.iloc[-1]
            src_node = src_node.drop(
                labels=["sort_1", "sort_2"],
                errors="ignore",
            )
            src_node = np.atleast_2d(src_node.to_numpy())
            for j, dst in enumerate(clusters):
                dst_df = df.query("sort_1 == @dst")
                dst_df = dst_df.set_index("sort_2")
                dst_node = dst_df.iloc[0]
                dst_node = dst_node.drop(
                    labels=["sort_1", "sort_2"],
                    errors="ignore",
                )
                dst_node = np.atleast_2d(dst_node.to_numpy())
                distance = scipy.spatial.distance.cdist(src_node, dst_node)
                distance_matrix[i, j] = distance

        G = nx.from_numpy_array(distance_matrix)
        tsp = nx.approximation.traveling_salesman_problem
        path = tsp(G, cycle=False)
        # Ensure the path contains no duplicates, but also preserve the order.
        path = list(dict.fromkeys(path))

        # Generate the new resulting dataframe
        # TODO: There may be a more performant way to do this.
        result = pd.DataFrame()
        for i in path:
            result = pd.concat([result, self._playlist.df.query("sort_1 == @i")])

        self._playlist.df = result

    def reorder(self):
        """Reorder playlist combining several techniques."""
        self._cluster()
        self._subcluster_opt()
        self._order_clusters()

    def suggest(self):
        """Suggest songs to add in the playlist."""
        return super().suggest()


class ChaosEvaluator(PlaylistEvaluatorBase):
    """Evaluate playlists try to make the least flowing playlist possible.

    Same as the TSPEvaluator, but maximize the distance instead.
    """

    def __init__(self, playlist: Playlist):
        super().__init__(playlist)

    def _preprocess_features(self, df: Optional[pd.DataFrame] = None):
        if df is None:
            df = self._playlist.df

        # Ordinal encode the artists
        # Ordinal encode the artists
        le = LabelEncoder()
        artist = le.fit_transform(df["artist"])
        artist = np.atleast_2d(artist).T
        df["artist_ord"] = artist

        # Assume all numeric features are valid input features
        numeric_df = df.select_dtypes(include=[np.number])

        mm_scaler = MinMaxScaler()
        numeric_df[:] = mm_scaler.fit_transform(numeric_df)
        scaled = numeric_df.to_numpy()

        return scaled

    def reorder(self):
        """Reorder the songs within the existing playlist.

        Inverse TSP problem.
        """
        feature_matrix = self._preprocess_features()
        distance_matrix = scipy.spatial.distance_matrix(
            feature_matrix,
            feature_matrix,
        )
        distance_matrix *= -1

        offset = abs(np.min(distance_matrix)) + 10
        distance_matrix += offset
        np.fill_diagonal(distance_matrix, 0)

        G = nx.from_numpy_array(distance_matrix)
        path = nx.approximation.traveling_salesman_problem(
            G,
            weight="weight",
            nodes=set(G.nodes),
            cycle=False,
        )

        if len(path) != len(distance_matrix):
            logger.warning(
                "Path length does not match distance matrix size (%d != %d)",
                len(path),
                len(distance_matrix),
            )
            path = list(dict.fromkeys(path))

        self._playlist.df["sort_1"] = path

    def suggest(self):
        """Suggest songs to be added into the playlist."""
        return super().suggest()


def simmer_playlist(
    p: Playlist,
    evaluator: Type[PlaylistEvaluatorBase],
    to_spotify: Optional[bool] = False,
) -> List[Track]:
    """Reorder / add songs to playlist for simmering.

    This is the main entrypoint to the playlist processing engine. It queries a
    playlist for all the required information about a playlist, then reorders
    the playlist (in-place) based on the evaluation of 'evaluator'.

    :param p: Playlist to be reordered.
    :param evaluator: Engine to use for the evaluation.
    :param to_spotify: Whether to write the modified playlist back to spotify.
    """
    p.df["sort_1"] = 0
    p.df["sort_2"] = 0

    e = evaluator(p)
    e.reorder()
    e.suggest()

    sort_columns = [i for i in p.df.columns if i.startswith("sort_")]
    p.df = p.df.sort_values(by=sort_columns)

    # Propogate local changes back to spotify playlist
    if to_spotify:
        p.to_spotify()

    cols_to_print = ["track", *sort_columns]
    print(p.df[cols_to_print])

    return list(p.df["track"])


if __name__ == "__main__":
    # For the sake of testing without spinning up the entire web application.
    import spotipy
    from dotenv import load_dotenv
    from spotipy.oauth2 import SpotifyOAuth

    LOG_LEVEL = logging.INFO
    format_ = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=format_, level=LOG_LEVEL)
    logger = logging.getLogger("SimmerTheToads")
    logger.setLevel(LOG_LEVEL)

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
        "Bring it on back copy": "5uelnwP0VJbVGgw8SsyTOZ",
    }

    cache_path = Path("./playlist.pickle")
    p = Playlist(spotify, playlists["Bring it on back copy"])

    simmer_playlist(
        p,
        ClusteringEvaluator,
        to_spotify=False,
    )
