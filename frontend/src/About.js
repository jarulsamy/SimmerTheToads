import React from "react";
import Person from "./Person";
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import JosephImage from "./images/Joseph.png";
import JoshImage from "./images/Josh.png";
import LonaImage from "./images/Lona.png";
import NatalieImage from "./images/Natalie.jpg";
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

function About() {
    let JosephText = "Joseph enjoys writing elegant and understandable code, mainly because he forgets how his own code works. " +
        "He worked on the fronted."
    let JoshText = "Josh is a VIM enthusiast (much less interesting than a Spotify enthusiast, he knows).He’ll primarily be working on the" +
        "backend and some of the ML functionality, and ensuring that everything runs smoothly, quickly, and intuitively."
    let LonaText = "Lona is a Spotify enthusiast and will primarily be helping with the API connections to both the backend and frontend." +
        "She’s also excited to make the application pretty and practical!"
    let NatalieText = "Natalie has experience with creating GUIs and is excited to experiment with react." +
        "Her role includes mostly frontend work (creating the website, adding user functionality," +
        "and making an aesthetic application)."

    return (
        <>
            {/* <Divider component="div" role="presentation">
                <Typography variant="h3">About the Project</Typography>
            </Divider> */}

            {/* Motivation Section */}
            <Grid container spacing={2}>
                <Grid item xs={3} />
                <Grid item xs={6}>
                    <Paper elevation={4} >
                        <Box m={2} >
                            <Typography variant="h4" color="text.primary">
                                Why We Made Simmer the Toads
                            </Typography>
                            <Typography variant="body3" color="text.secondary" paragraph="true" >
                                Consider this situation: you are stuck on a long road trip with many people you don't know. Naturally, you all have
                                differing music tastes, and so there is little cohesion between all the different songs you may add. Simmer The Toads
                                aims to solve this problem (and many others!) by creating a collaborative Spotify playlist platform, which not only
                                allows yourself and friends to create playlists but to seamlessly transition between music of one style to another.
                                To many of us, music has become more than a daily part of our lives. We listen to and explore new artists all the time.
                                A collaborative playlist service where we can come together to listen to the music that we already enjoy, but also
                                gently expand our tastes does not exist. Such a platform would aid in artist and genre discovery and even help get you
                                more acquainted with the music tastes of your friends.
                            </Typography>
                            <Typography variant="body3" color="text.secondary" paragraph="true">
                                When you boil frogs, you don’t put them in a hot pot initially - they’ll just jump straight out. You slowly but surely
                                turn up the heat. With our Spotify extension’s seamless musical genre transition tools, before you know it, you and your
                                friends (the proverbial frogs) will be “boiled” from Lana Del Rey’s dreamy chords to Nickelback’s 40 year old dad rock.
                                The affectionate nickname “Simmer the Toads”, is our homage to this adage, and to the existing Spotify extension named
                                “Boil The Frogs” that inspired this project. Simmer The Toads is a new Spotify extension that aims to refine a group’s
                                selection of varying artists and genres to create a seamless listening experience.
                            </Typography>
                        </Box>
                    </ Paper>
                </Grid>
                <Grid item xs={3} />
            </Grid>
            
            {/* Instructions on Use Section */}
            {/* pt={3} */}
            {/* <Box m={2} >
                <Divider variant="middle" component="div">
                    <Typography variant="h3">How to Use Simmer the Toads</Typography>
                </Divider>
            </Box> */}
            <Grid container spacing={2}>
                <Grid item xs={1} />
                <Grid item xs={6}>
                    <Paper elevation={4} >
                        <Box m={2} >
                            <Typography variant="h4" color="text.primary">
                                How To Use Simmer the Toads
                            </Typography>
                            <Typography variant="body3" color="text.secondary">
                                Simmer the Toads requires you to login to Spotify to function.
                                If you don't want to use an existing playlist you can make a playlist (in Spotify) to use on Simmer the Toads.
                                From there you can navigate to the main page and click the small simmer button under the playlist.
                                ...
                            </Typography>
                        </Box>
                    </Paper>
                </Grid>
                <Grid item xs={5} />
            </Grid>
            {/* How it Works*/}
            <Grid container spacing={2}>
                <Grid item xs={5} />
                <Grid item xs={6}>
                    <Paper elevation={4} >
                        <Box m={2} >
                            <Typography variant="h4" color="text.primary">
                                How It Works
                            </Typography>
                            <Typography variant="body3" color="text.secondary">
                                Simmer the Toads uses traveling salesman and ...
                                ...
                            </Typography>
                        </Box>
                    </Paper>
                </Grid>
                <Grid item xs={1} />
            </Grid>

            {/* The Use */}
            <Box m={2} >
                <Divider variant="middle" component="div">
                    {/* <Typography variant="h3">How to Use Simmer the Toads</Typography> */}
                </Divider>
            </Box>
            {/* <Divider component="div" role="presentation">
                <Typography variant="h3">Authors</Typography>
            </Divider> */}
            <Typography variant="h3" color="text.primary" align="center">
                Authors
            </Typography>
            <Grid container spacing={2}>
                <Grid item xs={3}>
                    <Person name="Joseph"
                        image={JosephImage}
                        description={JosephText}
                    />
                </Grid>
                <Grid item xs={3}>
                    <Person name="Josh"
                        image={JoshImage}
                        description={JoshText}
                    />
                </Grid>
                <Grid item xs={3}>
                    <Person name="Lona"
                        image={LonaImage}
                        description={LonaText}
                    />
                </Grid>
                <Grid item xs={3}>
                    <Person name="Natalie"
                        image={NatalieImage}
                        description={NatalieText}
                    />
                </Grid>
            </Grid>


        </>
    );
}

export default About;