# Recap 3

# Tasks Completed

We have written about 1k lines of code! Our deliverables are as follows:

### Frontend

- Rest API allows us to communicate between the frontend and backend.
- Website has pages, is viable, and is prettier!
- Frontend can take in songs then pass them to backend.
- API endpoints exist for all frontend components
- Frontend can talk to backend - API service!
- UI libraries have been selected!

### Backend

- We have a working sorting algorithm!
   - Agglomerative clustering is used to handle data. All songs are treated as individual clusters, and are continually merged into bigger clusters until all points are sorted.
   - We preprocess data by analysing Spotify's metadata on each song and cutting out all feaures below a 70% confidence level. This has allowed us to achieve significantly more accurate results, and reduce the amount of data we have to handle.
   - Data is encorded with numbers as ordinal values - i.e. artists are now treated as numbers
   - All of this is minmaxed and scaled for robustness.

# Successes

- MVP is done! We can now focus on adding more flavourful features.
- Our algorithm works + we're successfully sorting playlists.
- Our website works and looks decent.
- Backend/Frontend/Spotify passing works, so playlists can successfully be loaded from Spotify to the frontend, sorted in the backend, and passed back to Spotify.

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
- Develop algorithm for ordering clusters + inserting new songs to transition between clusters (TSP?)
- Chaos mode.

# Completion Confidence

- Lona: 5
- Josh: 5
- Natalie: 5
- Joseph: 5