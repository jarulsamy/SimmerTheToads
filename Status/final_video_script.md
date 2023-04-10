# Final Project Video Script

### Project Synopsis

Consider this situation: you are stuck on a long road trip with many people you don't know, and you are all queuing up songs on your favourite listening app for the drive. Naturally, you all have differing music tastes, and so there is little cohesion between all the different songs you may add, taking you on a musical rollercoaster between songs of varying genres, moods, and styles.

Simmer The Toads is our answer to this problem: a new Spotify extension that aims to refine a group’s selection of songs by bridging various artists and genres to create a seamless listening experience. With STT's musical genre transition tools, before you know it, you and your friends (the proverbial frogs) will be “boiled” from Lana Del Rey’s dreamy indie to Audioslave's guitar-fueled grunge.

To do this, we utilize ML techniques and hand-designed algorithms within clustering and graph optimization to organize playlists of varying songs, genres, and artists into a seamless (and well ordered) listening experience.

### Design Requirements & Specifications

Going into this project, we had a certain vision for how we hoped everything would pan out - which shifted slightly into the vision we're able to present to you today.

Our frontend was developed in Javascript, using MaterialUI and React. The frontend allows users to login to spotify and access their playlists. They're then able to be sent to the backend to be simmered. Afterwards, the completed playlist is sent back to the frontend and displayed for the user to save. 

We developed the backend primarily in Python, utilizing the lightweight Spotify library SpotiPy as a wrapper for the Spotify API. It’s connected to the frontend using Flask, a web application framework. Apart from our Machine Learning frameworks, the backend primarily handles user authentication and communicating between Spotify and the Frontend. This allows us to streamline the process of logging a user in, accessing their playlists, and then simmering and sending back a playlist to spotify.

Our ML techniques were done using the Python Libray SKLearn. The problem of reordering songs into some “optimal order” on a given playlist can be considered an unsupervised problem in ML. Essentially, this means that our data is not labelled or tagged, and our model is expected to analyze and find patterns inside of it. All our model has to base its evaluations off of is the playlist analytics we grab from Spotify at the time of evaluation. Given these constraints, we have a few options for Machine Learning algorithms. Out of these, we chose Clustering and TSP. Sklearn's Clustering Framework groups songs together based on similarities. TSP optimizes the distance between songs, essentially creating the optimal path of similarities between songs.

### Summry of Final Implementation
#### Design + Demonstration (voiceover!)
So, here's a brief video demonstration of our current product. I'm going to login using my Spotify account. Here, you can see all of your playlists, and select one or multiple to be simmered. I'm going to select this test playlist here...

After you've selected your playlist, you can choose one of our three simmering algorithms to use: Simmering, which is our proprietary clustering algorithm, Baking, which is our TSP algorithm, and Microwaving, which is our "just for fun" algorithm that tries to make the worst-organized playlist.
So let's simmer this playlist...

...and there we go! Let's take a look at our new, well-ordered playlist.

#### Limitations
We did face some challenges and limitations in developing Simmer the Toads. 
- Our first limitation was the fact that our model was completely unsupervised, meaning we have no metric to determine whether or not a playlist is objectively well-ordered. We used objective heuristics - i.e. personal preference - to evaluate our model. This wasn’t an ideal solution, but it did work.
- Another challenge was that building a website from scratch is very difficult - but we used MaterialUI to do a lot of the heavy lifting for us, allowing us to deploy a nice website in a short amount of time.
- Another limit is the speed of our algorithms - they're quite slow, as a playlist of 50 songs takes about 15 seconds. 

#### Future Direction
Overall, while we achieved many of our minimum viable product and reach goals, there are still a lot of prospects for STT in the future.
- In thefuture, developing an actual heuristic for playlist quality, such as a numeric rating, would be great for optimizing our performance.
- We'd also like to build out some sort of playlist staging interface, where a user can look at their final playlist, manually shuffle it around as they'd like, and see its various reorderings.
- STT initially was supposed to have a collaborative mode, where users and their friends can all input songs to create a playlist that can be simmered, but ultimately it was out of scope for the time we had - we'd really like to add that in the future.
- Lastly, speeding up our simmering algorithms was another task that was too time and resource heavy for us to try now, but is a definite hope for the future.

### Closing & Summary

Despite our challenges and the changes to our initial idea, we're proud of our final product. It accomplishes all the goals we set out for, and has really fulfilled the vision we had. We hope you love it just as much as we do!

Tada :)
