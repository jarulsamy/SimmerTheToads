# Final Project Video Script

### Project Synopsis

Consider this situation: you are stuck on a long road trip with many people you don't know, and you are all queuing up songs on your favourite listening app for the drive. Naturally, you all have differing music tastes, and so there is little cohesion between all the different songs you may add, taking you on a musical rollercoaster between songs of varying genres, moods, and styles.

Simmer The Toads is our answer to this problem: a new Spotify extension that aims to refine a group’s selection of songs by bridging various artists and genres to create a seamless listening experience. With STT's musical genre transition tools, before you know it, you and your friends (the proverbial frogs) will be “boiled” from Lana Del Rey’s dreamy indie to Audioslave's guitar-fueled grunge.

To do this, we utilize ML techniques and hand-designed algorithms within clustering and graph optimization to organize playlists of varying songs, genres, and artists into a seamless (and well ordered) listening experience.

### Design Requirements & Specifications

Going into this project, we had a certain vision for how we hoped everything would pan out - which shifted slightly into the vision we're able to present to you today.

Ideally, our frontend would allow users to lookup songs through Spotify to create a song list, which would then be sent to the backend to be simmered. Afterwards, the completed playlist would be sent back to the frontend and displayed for the user to save. 

We developed the backend primarily in Python, utilizing the lightweight Spotify library SpotiPy as a wrapper for the Spotify API. It’s connected to the frontend using Flask, a web application framework. Apart from our Machine Learning frameworks, the backend primarily handles user authentication and communicating between Spotify and the Frontend. This allows us to streamline the process of logging a user in, accessing their playlists, and then simmering and sending back a playlist to spotify.

Lastly, our Machine Learning components utiize 

### Summry of Final Implementation
>#### Design + Demonstration
>#### Limitations
>#### Future Direction

### Closing & Summary
