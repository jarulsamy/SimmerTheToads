# Recap 3

# Tasks Completed

We have written about 1k lines of code! Our deliverables are as follows:

### Frontend

- Website has pages, is viable, and is prettier!
- Frontend can take in songs then pass them to backend.
- API endpoints exist for MVP frontend components (playlist metadata, simmering
  actions, etc).
- Frontend can talk to backend - API service!
- UI libraries have been selected (Google's Material UI)!

### Backend

- We have a working sorting algorithm!
  - We preprocess data by analyzing Spotify's metadata on each song and cutting
    out all features below a 70% confidence level. This has allowed us to
    achieve significantly more accurate results, and reduce the amount of data
    we have to handle. All of this is scaled for robustness.
  - Categorical features (artists, genre, etc) are encoded as ordinal values.
  - Time series data is averaged into sections and encoded as several columns of
    ordinal values.
  - Agglomerative clustering is used to cluster data. All songs are treated as
    individual clusters and are continually merged into bigger clusters until
    all points are sorted.
  - Tracks within clusters are ordered by computing an euclidean distance matrix
    for all the track features and calculating the minimum length tour (TSP).

# Successes

- MVP is done! We can now focus on adding more flavourful features.
- Our algorithm works + we're successfully sorting playlists.
- Our website works and looks decent.
- Backend/Frontend/Spotify passing works, so playlists can successfully be
  loaded from Spotify to the frontend, sorted in the backend, and passed back to
  Spotify.

# Challenges

- Worried about MVP not getting completed in time - thankfully overcame! (:

# Goals for the Next 3 Weeks

### Frontend

- Prettify things further
- Fix login authentication
- Migrate over to MaterialUI for easier mobile integration
- Add song lookup features + ability to create new playlists
- "Staging" page for simmering to allow for more interactibility

### Backend

- Also fix login authentication
- Develop some alternative algorithms for playlist reordering (address bias,
  etc.).
- Chaos mode (NASA space entropy?!).

# Completion Confidence

- Lona: 5
- Josh: 5
- Natalie: 5
- Joseph: 5
