from copy import deepcopy

import pytest

from SimmerTheToads.engine import Playlist, grouper

AUDIO_ANALYSIS = {
    "meta": {
        "analyzer_version": "4.0.0",
        "platform": "Linux",
        "detailed_status": "OK",
        "status_code": 0,
        "timestamp": 1495193577,
        "analysis_time": 6.93906,
        "input_process": "libvorbisfile L+R 44100->22050",
    },
    "track": {
        "num_samples": 4585515,
        "duration": 207.95985,
        "sample_md5": "string",
        "offset_seconds": 0,
        "window_seconds": 0,
        "analysis_sample_rate": 22050,
        "analysis_channels": 1,
        "end_of_fade_in": 0,
        "start_of_fade_out": 201.13705,
        "loudness": -5.883,
        "tempo": 118.211,
        "tempo_confidence": 0.73,
        "time_signature": 4,
        "time_signature_confidence": 0.994,
        "key": 9,
        "key_confidence": 0.408,
        "mode": 0,
        "mode_confidence": 0.485,
        "codestring": "string",
        "code_version": 3.15,
        "echoprintstring": "string",
        "echoprint_version": 4.15,
        "synchstring": "string",
        "synch_version": 1,
        "rhythmstring": "string",
        "rhythm_version": 1,
    },
    "bars": [{"start": 0.49567, "duration": 2.18749, "confidence": 0.925}],
    "beats": [{"start": 0.49567, "duration": 2.18749, "confidence": 0.925}],
    "sections": [
        {
            "start": 0,
            "duration": 6.97092,
            "confidence": 1,
            "loudness": -14.938,
            "tempo": 113.178,
            "tempo_confidence": 0.647,
            "key": 9,
            "key_confidence": 0.297,
            "mode": -1,
            "mode_confidence": 0.471,
            "time_signature": 4,
            "time_signature_confidence": 1,
        }
    ],
    "segments": [
        {
            "start": 0.70154,
            "duration": 0.19891,
            "confidence": 0.435,
            "loudness_start": -23.053,
            "loudness_max": -14.25,
            "loudness_max_time": 0.07305,
            "loudness_end": 0,
            "pitches": [0.212, 0.141, 0.294],
            "timbre": [42.115, 64.373, -0.233],
        }
    ],
    "tatums": [{"start": 0.49567, "duration": 2.18749, "confidence": 0.925}],
}

AUDIO_FEATURES = {
    "acousticness": 0.00242,
    "analysis_url": "https://api.spotify.com/v1/audio-analysis/2takcwOaAZWiXQijPHIx7B",
    "danceability": 0.585,
    "duration_ms": 237040,
    "energy": 0.842,
    "id": "2takcwOaAZWiXQijPHIx7B",
    "instrumentalness": 0.00686,
    "key": 9,
    "liveness": 0.0866,
    "loudness": -5.883,
    "mode": 0,
    "speechiness": 0.0556,
    "tempo": 118.211,
    "time_signature": 4,
    "track_href": "https://api.spotify.com/v1/tracks/2takcwOaAZWiXQijPHIx7B",
    "type": "audio_features",
    "uri": "spotify:track:2takcwOaAZWiXQijPHIx7B",
    "valence": 0.428,
}

PLAYLIST = {
    "collaborative": True,
    "description": "string",
    "external_urls": {"spotify": "string"},
    "followers": {"href": "string", "total": 0},
    "href": "string",
    "id": "string",
    "images": [
        {
            "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228",
            "height": 300,
            "width": 300,
        }
    ],
    "name": "string",
    "owner": {
        "external_urls": {"spotify": "string"},
        "followers": {"href": "string", "total": 0},
        "href": "string",
        "id": "string",
        "type": "user",
        "uri": "string",
        "display_name": "string",
    },
    "public": True,
    "snapshot_id": "string",
    "tracks": {
        "href": "https://api.spotify.com/v1/me/shows?offset=0&limit=20",
        "limit": 20,
        "next": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
        "offset": 0,
        "previous": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
        "total": 4,
        "items": [
            {
                "added_at": "2019-08-24T14:15:22Z",
                "added_by": {
                    "external_urls": {"spotify": "string"},
                    "followers": {"href": "string", "total": 0},
                    "href": "string",
                    "id": "string",
                    "type": "user",
                    "uri": "string",
                },
                "is_local": True,
                "track": {
                    "album": {
                        "album_type": "compilation",
                        "total_tracks": 9,
                        "available_markets": ["CA", "BR", "IT"],
                        "external_urls": {"spotify": "string"},
                        "href": "string",
                        "id": "2up3OPMp9Tb4dAKM2erWXQ",
                        "images": [
                            {
                                "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228",
                                "height": 300,
                                "width": 300,
                            }
                        ],
                        "name": "string",
                        "release_date": "1981-12",
                        "release_date_precision": "year",
                        "restrictions": {"reason": "market"},
                        "type": "album",
                        "uri": "spotify:album:2up3OPMp9Tb4dAKM2erWXQ",
                        "copyrights": [{"text": "string", "type": "string"}],
                        "external_ids": {
                            "isrc": "string",
                            "ean": "string",
                            "upc": "string",
                        },
                        "genres": ["Egg punk", "Noise rock"],
                        "label": "string",
                        "popularity": 0,
                        "album_group": "compilation",
                        "artists": [
                            {
                                "external_urls": {"spotify": "string"},
                                "href": "string",
                                "id": "string",
                                "name": "string",
                                "type": "artist",
                                "uri": "string",
                            }
                        ],
                    },
                    "artists": [
                        {
                            "external_urls": {"spotify": "string"},
                            "followers": {"href": "string", "total": 0},
                            "genres": ["Prog rock", "Grunge"],
                            "href": "string",
                            "id": "string",
                            "images": [
                                {
                                    "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228",
                                    "height": 300,
                                    "width": 300,
                                }
                            ],
                            "name": "string",
                            "popularity": 0,
                            "type": "artist",
                            "uri": "string",
                        }
                    ],
                    "available_markets": ["string"],
                    "disc_number": 0,
                    "duration_ms": 0,
                    "explicit": True,
                    "external_ids": {
                        "isrc": "string",
                        "ean": "string",
                        "upc": "string",
                    },
                    "external_urls": {"spotify": "string"},
                    "href": "string",
                    "id": "string",
                    "is_playable": True,
                    "linked_from": {},
                    "restrictions": {"reason": "string"},
                    "name": "string",
                    "popularity": 0,
                    "preview_url": "string",
                    "track_number": 0,
                    "type": "track",
                    "uri": "string",
                    "is_local": True,
                },
            }
        ],
    },
    "type": "string",
    "uri": "string",
}

TRACKS = {
    "href": "https://api.spotify.com/v1/me/shows?offset=0&limit=20",
    "limit": 20,
    "next": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
    "offset": 0,
    "previous": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
    "total": 4,
    "items": [
        {
            "added_at": "2019-08-24T14:15:22Z",
            "added_by": {
                "external_urls": {"spotify": "string"},
                "followers": {"href": "string", "total": 0},
                "href": "string",
                "id": "string",
                "type": "user",
                "uri": "string",
            },
            "is_local": True,
            "track": {
                "album": {
                    "album_type": "compilation",
                    "total_tracks": 9,
                    "available_markets": ["CA", "BR", "IT"],
                    "external_urls": {"spotify": "string"},
                    "href": "string",
                    "id": "2up3OPMp9Tb4dAKM2erWXQ",
                    "images": [
                        {
                            "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228",
                            "height": 300,
                            "width": 300,
                        }
                    ],
                    "name": "string",
                    "release_date": "1981-12",
                    "release_date_precision": "year",
                    "restrictions": {"reason": "market"},
                    "type": "album",
                    "uri": "spotify:album:2up3OPMp9Tb4dAKM2erWXQ",
                    "copyrights": [{"text": "string", "type": "string"}],
                    "external_ids": {
                        "isrc": "string",
                        "ean": "string",
                        "upc": "string",
                    },
                    "genres": ["Egg punk", "Noise rock"],
                    "label": "string",
                    "popularity": 0,
                    "album_group": "compilation",
                    "artists": [
                        {
                            "external_urls": {"spotify": "string"},
                            "href": "string",
                            "id": "string",
                            "name": "string",
                            "type": "artist",
                            "uri": "string",
                        }
                    ],
                },
                "artists": [
                    {
                        "external_urls": {"spotify": "string"},
                        "followers": {"href": "string", "total": 0},
                        "genres": ["Prog rock", "Grunge"],
                        "href": "string",
                        "id": "string",
                        "images": [
                            {
                                "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228",
                                "height": 300,
                                "width": 300,
                            }
                        ],
                        "name": "string",
                        "popularity": 0,
                        "type": "artist",
                        "uri": "string",
                    }
                ],
                "available_markets": ["string"],
                "disc_number": 0,
                "duration_ms": 0,
                "explicit": True,
                "external_ids": {"isrc": "string", "ean": "string", "upc": "string"},
                "external_urls": {"spotify": "string"},
                "href": "string",
                "id": "string",
                "is_playable": True,
                "linked_from": {},
                "restrictions": {"reason": "string"},
                "name": "string",
                "popularity": 0,
                "preview_url": "string",
                "track_number": 0,
                "type": "track",
                "uri": "string",
                "is_local": True,
            },
        }
    ],
}

track = PLAYLIST["tracks"]["items"][0]
# Duplicate a single track
for i in range(25):
    PLAYLIST["tracks"]["items"].append(track)

track = TRACKS["items"][0]
for i in range(25):
    TRACKS["items"].append(track)

from pprint import pprint

pprint(TRACKS)


class SpotifyMock:
    """Mock the necessary portions of the Spotify WebAPI."""

    def __init__(self, playlist: dict, n_tracks=None):
        self._playlist = playlist
        self._playlist_track_ids = [
            i["track"]["id"] for i in self._playlist["tracks"]["items"]
        ]
        if n_tracks is None:
            self.n_tracks = len(self._playlist_track_ids)
        else:
            self.n_tracks = n_tracks

    def playlist(self, id):
        return self._playlist

    def user_playlist_tracks(self, playlist_id):
        tracks = TRACKS["items"][: self.n_tracks]
        my_resp = deepcopy(TRACKS)
        my_resp["items"] = tracks
        return my_resp

        # items = self._playlist["tracks"]["items"][: self.n_tracks]
        # my_tracks = deepcopy(self._playlist)
        # my_tracks["tracks"]["items"] = items

        # return my_tracks

    def playlist_replace_items(self):
        raise NotImplementedError

    def next(self, id):
        return {"next": None, "items": []}

    def audio_analysis(self, id):
        # Just return a dummy audio analysis for any id.
        return AUDIO_ANALYSIS

    def audio_features(self, id):
        # Just return a dummy audio feature set for any id.
        return [AUDIO_FEATURES]


def test_grouper_even():
    input_ = [1, 2, 3, 4]
    output = list(grouper(input_, 2))
    expected = [(1, 2), (3, 4)]
    assert output == expected


def test_grouper_odd():
    input_ = [1, 2, 3, 4, 5]
    output = list(grouper(input_, 2))
    expected = [(1, 2), (3, 4)]
    assert output == expected


def test_construct_playlist():
    spotify = SpotifyMock(PLAYLIST)
    Playlist(spotify, "some mock id")


def test_construct_empty_playlist_raises():
    spotify = SpotifyMock(PLAYLIST, n_tracks=0)
    with pytest.raises(ValueError):
        Playlist(spotify, "some mock id")


def test_construct_playlist_with_single_track():
    spotify = SpotifyMock(PLAYLIST, n_tracks=1)
    Playlist(spotify, "some mock id")
