import React from "react";
import Person from "./Person";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import JosephImage from "./images/Joseph.png";
import JoshImage from "./images/Josh.png";
import LonaImage from "./images/Lona.png";
import NatalieImage from "./images/Natalie.jpg";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";

function About() {
  let JosephText = `Joseph enjoys writing elegant and understandable code,
  mainly because he forgets how his own code works. He worked on the
  fronted.`;

<<<<<<< HEAD
  let JoshText = `Josh enjoys contributing to many open source projects and
  tinkering with Linux. "He is a WRSP Scholar and works in the UWyo MALLET lab
  as an undergraduate research assistant. Currently, he is conducting empircal
  analysis on modern implementations of quicksort and exploring new optimization
  techniques to improve performance.`;
=======
    return (
        <Box style={{ overflow: "scroll" }}>
            {/* <Divider component="div" role="presentation">
                <Typography variant="h3">About the Project</Typography>
            </Divider> */}
>>>>>>> main

  let LonaText = `Lona is a San Diego native with interests in Machine Learning,
  and a focus in natural language processing.  She currently works as an
  undergraduate research assistant at the UWyo MALLET Lab.  Her current research
  is a comparison of how common ML tasks are done between the MLR3, SKLearn, and
  MLJulia packages.  Outside of her research, she also works as a Teaching
  Assistant for the Intro to Computer Science course at UWyo, and as a student
  mentor for the Office of Student Success & Graduation.  Her hobbies include
  cooking, making great coffee, and pilates. She's also a dance instructor of 3
  years!`;

  let NatalieText = `Natalie is a senior undergraduate in Computer Science. She
  works in the UW MALLET Lab on a project involving editing and authoring
  sections of a textbook on a popular machine earning package in R. She also
  works in Computational Chemistry Lab creating a user interface for a project
  on electrical thermal transport. She is passionate about Equality in Computing
  (EIC) and founded a club by the same name. She has organized four popular
  bookclubs on equality issues in tech for EIC over the course of her time at
  UW. You might not be surprised that she spends her free time reading!`;

  return (
    <Box style={{ overflow: "auto" }}>
      <Grid container spacing={2} style={{ overflow: "auto" }}>
        <Grid item xs={3} />
        <Grid item xs={6}>
          <Paper
            elevation={4}
            sx={{ color: "text.secondary", bgcolor: "#a3ac88" }}
          >
            <Box m={2}>
              <Typography variant="h4">Why We Made Simmer the Toads</Typography>
              <Typography variant="body3" paragraph="true">
                Consider this situation: You are stuck on a long road trip with
                many people you don't know, and you are all queuing up songs on
                your favourite listening app for the drive. Naturally, you all
                have differing music tastes, and so there is little cohesion
                between all the different songs you may add.
              </Typography>
              <Typography variant="body3" paragraph="true">
                Our project, Simmer The Toads is our answer to this problem: a
                new Spotify extension that aims to refine a group’s selection of
                songs by bridging various artists and genres to create a
                seamless listening experience.
              </Typography>
              <Typography variant="body3" paragraph="trueg">
                To many of us, music has become more than a daily part of our
                lives. We listen to and explore new artists all the time. STT
                aims to be a playlist service where we can come together to
                listen to the music that we already enjoy, but also gently
                expand our tastes does not exist. Such a platform would aid in
                artist and genre discovery and even help get you more acquainted
                with the music tastes of your friends.
              </Typography>
              <Typography variant="body3" paragraph="true">
                When you boil frogs, you don't put them in a hot pot initially -
                they'll just jump straight out. You slowly but surely turn up
                the heat. With our Spotify extension's seamless musical genre
                transition tools, before you know it, you and your friends (the
                proverbial frogs) will be “boiled” from Lana Del Rey's dreamy
                chords to Nickelback's 40 year old dad rock. The affectionate
                nickname “Simmer the Toads”, is our homage to this adage, and to
                the existing Spotify extension named “Boil The Frogs” that
                inspired this project. Simmer The Toads is a new Spotify
                extension that aims to refine a group's selection of varying
                artists and genres to create a seamless listening experience.
              </Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={3} />
      </Grid>

      <Grid container spacing={2} style={{ overflow: "auto" }}>
        <Grid item xs={1} />
        <Grid item xs={6}>
          <Paper
            elevation={4}
            sx={{ color: "text.primary", bgcolor: "#B38D97" }}
          >
            <Box m={2}>
              <Typography variant="h4">How To Use Simmer the Toads</Typography>
              <Typography variant="body3">
                Simmer the Toads requires you to login to Spotify first. You'll
                be able to access your playlists from the main page. Click the
                playlists you want to simmer, select your algorithm, and enjoy!
                Note that STT does overwrite your existing playlists - to avoid
                this, we reccomend duplicating your playlist through Spotify.
              </Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={5} />
      </Grid>
      {/* How it Works*/}
      <Grid container spacing={2} style={{ overflow: "auto" }}>
        <Grid item xs={5} />
        <Grid item xs={6}>
          <Paper elevation={4} sx={{ color: "#ECBEB4", bgcolor: "#422040" }}>
            <Box m={2}>
              <Typography variant="h4">How It Works</Typography>
              <Typography variant="body3" paragraph="true">
                First, our algorithm analyses metadata scraped from Spotify
                about each song. We can get simple information such as artist,
                genre, and album, but Spotify also allows us to pull more
                detailed features out, such as acousticness, valence, mood,
                energy, and danceability. All of this data is then analysed and
                preprocessed.
              </Typography>
              <Typography variant="body3" paragraph="true">
                Next, we optimize the ordering of these songs. They’re sorted
                into clusters based on their similarity. Each cluster is then
                organized in some optimal order based on its “distance”, or
                feature closeness, from other clusters.
              </Typography>
              <Typography variant="body3" paragraph="true">
                Lastly, we curate additional transition songs using Spotify’s
                recommendation API. These songs are added between clusters to
                make seamless listening transitions.
              </Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={1} />
      </Grid>

      <Box m={2}>
        <Divider variant="middle" component="div"></Divider>
      </Box>
      <Typography variant="h3" color="text.primary" align="center">
        Authors
      </Typography>
      <Grid container spacing={2} style={{ overflow: "auto" }}>
        <Grid item xs={3}>
          <Person name="Joseph" image={JosephImage} description={JosephText} />
        </Grid>
        <Grid item xs={3}>
          <Person name="Josh" image={JoshImage} description={JoshText} />
        </Grid>
        <Grid item xs={3}>
          <Person name="Lona" image={LonaImage} description={LonaText} />
        </Grid>
        <Grid item xs={3}>
          <Person
            name="Natalie"
            image={NatalieImage}
            description={NatalieText}
          />
        </Grid>
      </Grid>
    </Box>
  );
}

export default About;
