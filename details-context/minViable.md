# Minimum Viable Product

## User Interface - Frontend

A website with the following core components:

- A login with Spotify button/link.
- List/table of all the current user's playlists.
- Ability to select a playlist and request reordering ('simmering').
- A way to view the resulting playlist and to confirm whether or not to write
  the changes back to the original Spotify playlist.

## Playlist Evaluator and REST API - Backend

- Maintain Spotify login state for users.
- Retrieve all playlists from the current user.
- Analyze an existing playlist, reorder, and optionally add songs.
- Output the result in some serializable fashion and optionally write the
  changes back to the original Spotify playlist.
