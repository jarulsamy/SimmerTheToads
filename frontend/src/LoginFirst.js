import React from "react";
// import Box from "@mui/material/Box";
import { Container, Typography } from "@mui/material";
import { Box, Grid } from "@mui/material";
import Paper from "@mui/material/Paper";
import NiceImage from "./NiceImage";
import boiling_froggie from "./images/loading_simmer.gif";

// sx={{background: 'linear-gradient(to bottom, #F1DAC4, #ECBEB4)', width: '100%', height: '100%'}}

function LoginFirst() {
  return (
    <Box>
      <NiceImage image={boiling_froggie}/>
      <Typography padding={4} fontSize="25px" align="center">
        Oh, hey there :) We're Simmer the Toads: a Spotify extention that utilizes Machine
        Learning techniques to elegantly organize your playlists, creating seamless transitions between songs of varying genres, artists, and moods.
      </Typography>
      <Typography padding={4} variant="h5">
        We developed three algorithms for you to choose from:
      </Typography>

      <Grid container justifyContent="space-evenly">
        <Grid sx={{ width: "25%" }} item justifyContent={"center"}>
          <Paper elevation={3}>
            <Box padding={3} color="text.secondary" bgcolor="#a3ac88">
              <Typography variant="h4">Simmer</Typography>
              <Typography variant="body2">
                A clustering based approach that will smooth out the transitions
                between all the different genres in your playlist by grouping
                them with similar songs.
              </Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid sx={{ width: "25%" }} item>
          <Paper elevation={3}>
            <Box padding={3} color="text.primary" bgcolor="#B38D97">
              <Typography variant="h4">Bake</Typography>
              <Typography variant="body2">
                A TSP-based approach that will organize your playlist based on
                finding the shortest musical path between your songs.
              </Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid sx={{ width: "25%" }} item>
          <Paper elevation={3}>
            <Box padding={3} color="#ECBEB4" bgcolor="#422040">
              <Typography variant="h4">Microwave</Typography>
              <Typography variant="body2">
                A chaotic method that will do its very best to make your
                playlist as transitionally unpleasant as possible.
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      <Typography padding={4} variant="h4">
        To use these, please login to your Spotify account!
      </Typography>
      <Box
      sx={{
        height: 200,
        backgroundColor: 'transparent',
      }}
    />
    </Box>
  );
}

export default LoginFirst;