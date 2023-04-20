import React from "react";
// import Box from "@mui/material/Box";
import { Container, Typography } from "@mui/material";
import { Box, Grid } from "@mui/material";
import Paper from "@mui/material/Paper";
import NiceImage from "./NiceImage";
import boiling_froggie from "./images/loading_simmer.gif";
import baking_froggie from "./images/loading_baking.gif";
import microwaving_froggie from "./images/loading_microwaving.gif";
import SimmeringCard from "./SimmeringCard";

// sx={{background: 'linear-gradient(to bottom, #F1DAC4, #ECBEB4)', width: '100%', height: '100%'}}

function LoginFirst() {
  return (
    <Box>
      {/* <NiceImage image={boiling_froggie} /> */}
      <Typography padding={4} fontSize="25px" align="center">
        Oh, hey there :) We're Simmer the Toads: a Spotify extention that
        utilizes Machine Learning techniques to elegantly organize your
        playlists, creating seamless transitions between songs of varying
        genres, artists, and moods.
      </Typography>
      <Typography padding={4} fontSize="25px" align="center">
        We developed three algorithms for you to choose from:
      </Typography>

      <Grid container justifyContent="space-evenly">
        <Grid sx={{ width: "25%" }} item justifyContent={"center"}>
            <SimmeringCard name="Simmer" image= {boiling_froggie} bgColor={"#a3ac88"} textColor={"text.secondary"} description={"A clustering based approach that will smooth out the transitions between all the different genres in your playlist by grouping them with similar songs."}/>
        </Grid>
        <Grid sx={{ width: "25%" }} item>
            {/* bgcolor="#B38D97"> */}
              <SimmeringCard name="Bake" image={baking_froggie} bgColor={"#B38D97"} textColor={"text.primary"} description={"A TSP-based approach that will organize your playlist based on finding the shortest musical path between your songs."} />
        </Grid>
        <Grid sx={{ width: "25%" }} item>
          <SimmeringCard name="Microwave" image={microwaving_froggie} bgColor={"#422040"} textColor={"#ECBEB4"} description={"A chaotic method that we added just for fun - it will do its very best to make your playlist as transitionally unpleasant as possible."} />
        </Grid>
      </Grid>

      <Typography padding={4} variant="h4" align="center">
        To use these, please login to your Spotify account!
      </Typography>
    </Box>
  );
}

export default LoginFirst;
