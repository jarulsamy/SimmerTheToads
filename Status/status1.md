# Recap

# Tasks Completed

We have written 1572 lines of code!! :D Our deliverables are as follows:

### Frontend - Natalie & Joseph

- Barebones site is complete
- Songs can be "obtained" from the user, no authentication for their existence
  on Spotify yet
- Songs can be sent to backend
- Not one, not two, but **THREE** pages!

### Backend - Lona & Joshy

- User account authentication flow and callbacks with Spotify are all tested and
  ready.
- Asynchronous, parallel fetching of all metadata about tracks and playlists.
- Graphs!! You want 'em? We got em! We added lots of ways to visualize all this
  data!

  ![](https://user-images.githubusercontent.com/14321139/214881542-4c32855a-c051-47e9-a2f7-4f18acf5b76a.png)

- Version 1 of WIP algorithm to reorder songs
- Ability to reorder songs exists & can be accessed manually from backend
- Options to serialize playlists and tracks to JSON/pickles.

### Miscellaneous Other Tasks

- We talked to Ward, and have a deployment strategy!
- Test playlists exist (thanks to Lona's absurdly large song database), more to
  come.

# Goals for the Next 3 Weeks

### Frontend

- Prettify + make it less barebones
- Spotify Authentication button
- Mock sketches for ideal layout

### Backend

- What are our quantifiers to organize playlists? We need to design a better
  algorithm to:

  - Quantify how homogeneous a given playlist is.

  - Utilize all the data we are provided to create an optimal playlist (graph
    optimization problem).

- Create new reordered playlist on Spotify, as opposed to JSON
- Frontend/Backend Passing
- Misc Spotify Shenanigans (performance of metadata fetching)

### Miscellaneous Other Tasks

- More playlists to use for comparison
