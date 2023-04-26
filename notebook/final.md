# Final Project Notebook

## Synopsis of Project Goals

- Create a collaborative Spotify playlist platform.
- Have a visually appealing and intuitive frontend.
- Optimize playlists to seamlessly transition from one music style to another.
- Utilize existing Spotify recommendation APIs to analyze songs within a
  playlist, identify distinct genres and styles, and suggest similar songs.
- Allow users to refine their playlists quickly, intuitively, and easily.

## Links to Written Status Updates

- [Status #1](Status/status1.md)
- [Status #2](Status/status2.md)
- [Status #3](Status/status3.md)
- [Status #4](Status/status4.md)

## Links to Videos

- [Demo Video](https://drive.google.com/file/d/1P7semxK-kGSKX0Kd9hiwo2uvoAK_8abu/view?usp=sharing)

## Project Planning And Execution

- [Design Requirements and Specification](https://docs.google.com/document/d/1mxL4wcjIboUZs82ka1uiGlvUL_izlJdRB-PtG3yicJk/edit?usp=sharing)
- [System Concept Diagram](ElevatorPitch/systemconceptdiagram.pdf)
- [Asana Plan](https://app.asana.com/0/1203117920538793/1203117920538793)
- Original MVP Plan

  - Frontend - ReactJS
    1. Get web server running + bare bones website.
    2. Create input fields for songs
       - Create field where user can input a list of song names.
       - Add ability to reorder within this list.
    3. Add Spotify authentication
    4. Submit song list
       - Retrieve list from input method.
       - Send to backend via REST API endpoint.
    5. Communications with backend
       - Create functions that format data nicely to backend.
    6. Display finished playlist.
       - Retrieve result from backend.
       - Allow user to audit the suggested playlist alterations.
  - Backend + ML - Flask
    1. Create some interface to talk to Spotify APIs and retrieve metadata about
       songs.
    2. Represent the playlist as a graph.
    3. Organize songs within the playlist.
    4. Determine where to add transition songs.
    5. Find songs of similar genres to fill gaps.
    6. Format the result back into a Spotify playlist.
    7. Send resulting playlist back to frontend.
  - Integration
    - Have some interface for passing data between the frontend and backend.
    - Allow the frontend to lookup songs with Spotify integration.
    - Authorization scopes from Spotify.

- Deviations from the Original Plan
  - Frontend
    - Allow the user to select an existing Spotify playlist rather than building
      one manually.
    - Add MaterialUI to make development quicker and easier.
    - Not responsible for Spotify authentication.
    - Modern layout and pleasing appearance.
    - Shows playlist cover art.
    - No interface for confirming the "simmering"
  - Backend + ML
    - Use SpotiPy to make Spotify API interactions quicker and easier.
    - Allow users to login to Spotify using OAuth2.
    - Three primary playlist "Simmering" methods
      - Simmering - Cluster playlist using agglomerative clustering and add
        songs between clusters.
      - Baking - Treat playlist as a directed graph and find the minimal TSP
        tour. Add songs within large edges.
      - Microwave - Same as baking but find the maximal TSP tour.
  - Integration
    - Frontend cannot lookup/search songs through the backend.

## Summary of Final Implementation

### Design

(TODO: A frontend person is much more qualified to talk about this)

### Limitations

- Somewhat slow to simmer -- 15 seconds per 50 songs.
- Currently no way to confirm or undo the simmering process.
- Not publicly usable (yet).
- Excessively large playlists aren't supported (Spotify rate limit).
- Mobile support is questionable.
- No collaborative mode.

### Future Directions

- Speedup our simmering algorithms.
- Add a staging interface so that users can edit/confirm/abandon changes before
  committing them to the original Spotify playlist.
- Pass Spotify quota extension requirements to become available to the general
  public.
- Create a more objective heuristic for playlist quality.
- Better mobile support.
- Collaborative mode.

### Statement of Work

#### Team

(TODO)

#### Josh

(TODO)

#### Natalie

(TODO)

#### Lona

(TODO)

#### Joseph

(TODO)

## Reflection

### Lessons Learned

(TODO)

### "If we had to do it all over again"

(TODO)

### Advice for Future Groups

(TODO)
