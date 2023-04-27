# Final Project Notebook

## Synopsis of Project Goals

- Create a collaborative Spotify playlist platform.
- Have a visually appealing and intuitive frontend.
- Optimize playlists to seamlessly transition from one music style to another.
- Utilize existing Spotify recommendation APIs to analyze songs within a
  playlist, identify distinct genres and styles, and suggest similar songs.
- Allow users to refine their playlists quickly, intuitively, and easily.

## Links to Written Status Updates

- [Status #1](/Status/status1.md)
- [Status #2](/Status/status2.md)
- [Status #3](/Status/status3.md)
- [Status #4](/Status/status4.md)

## Links to Videos

- [Demo Video](https://drive.google.com/file/d/1P7semxK-kGSKX0Kd9hiwo2uvoAK_8abu/view?usp=sharing)

## Project Planning And Execution

- [Design Requirements and Specification](https://docs.google.com/document/d/1mxL4wcjIboUZs82ka1uiGlvUL_izlJdRB-PtG3yicJk/edit?usp=sharing)
- [System Concept Diagram](/ElevatorPitch/systemconceptdiagram.pdf)
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

We wanted our website to allow for these features:

- Users can login to their Spotify account through our website
- Users can select one or more playlists at a time
- Playlists can be Simmered, Baked, or Microwaved (names for our playlist
  optimization algorithms)

Other than these features, we wanted our website to be cohesive, aesthetic, and
cute. We wanted our project to have an abundance of personality so that we could
have fun with it. This meant that we wanted the design to include artistic
assets, colors and cute fonts.

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

We were able to create three hand designed algorithms (Simmer, Bake, Microwave)
that we wrapped into a Spotify Extension. We also created a website so that
users can utilize this Spotify Extension. This website has character and is fun
and easy to use. The backend is well designed and efficient.

#### Josh

I primarily worked on the backend. I implemented our Spotify API integration,
allowing users to login with their existing Spotify credentials, view and select
their playlists, and also researched and developed our three primary playlist
evaluation and optimization algorithms. I also developed integration strategies
for the frontend and handled deployment.

#### Natalie

I worked on creating the frontend. I combined and tailored MUI components to
create the features of our website (minus the Spotify login feature). I
implemented the ability to select one or more playlists to optimize. I also
implemented the state passing between the playlist cards and simmering buttons,
as well as the API calls to the backend. I helped Lona with some aesthetic
decisions.

#### Lona

I helped support Josh in developing the Machine Learning algorithms. I also
created art mock-ups for the site, and assisted Natalie in prettifying the
frontend! I also wrote status updates and supplemental materials for our
documentation.

#### Joseph

Joseph worked on the frontend collaborating with Natalie. I designed and
implemented the About page on the website using React at first and then again
with Material UI after we switched to using that library. I also created some of
the graphics for the presentation.

## Reflection

### Lessons Learned

- Have someone to manage github well
- Delegate tasks and separate out components for an easier workflow
- Use libraries - try to build out nothing from scratch!
- Don't be afraid to pivot from your vision - be flexible and adapt to
  difficulties

### "If we had to do it all over again"

- Start in MaterialUI
- Started Staging Interface earlier
- Instead of a waterfall approach, use an agile approach

### Advice for Future Groups

- Plan ahead, and plan thoroughly. One thing that really helped us was having
  thorough plans for frontend, backend, and ML
- Ask for help from fellow students and faculty - perspective was really
  important for us
- Plan to be done a month early - you will need the extra time and wiggle room
  with scheduling
- Meet frequently - once a week ideally, and in person if you can
- Make it fun and something you're proud of - it's better to have your project
  be a little weird than boring
