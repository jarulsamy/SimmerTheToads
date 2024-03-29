import React from "react";
import { Container, Typography } from "@mui/material";
import { Box, Grid } from "@mui/material";
import Paper from "@mui/material/Paper";
import boiling_froggie from "./images/loading_simmer.gif";
import baking_froggie from "./images/loading_baking.gif";
import microwaving_froggie from "./images/loading_microwaving.gif";
import SimmeringCard from "./SimmeringCard";

function LoginFirst() {
  return (
    <Box>
      <Typography padding={4} fontSize="25px" align="center">
        <Container>
          Oh, hey there :) We're Simmer the Toads: a Spotify extention that
          utilizes Machine Learning techniques to elegantly organize your
          playlists, creating seamless transitions between songs of varying
          genres, artists, and moods.
        </Container>
      </Typography>
      <Typography padding={4} fontSize="25px" align="center">
        We developed three algorithms for you to choose from:
      </Typography>

      <Grid container justifyContent="space-evenly">
        <Grid sx={{ width: "25%" }} item justifyContent={"center"}>
          <Paper elevation={4}>
            <SimmeringCard
              name="Simmer"
              image={boiling_froggie}
              bgColor={"#a3ac88"}
              textColor={"text.secondary"}
              description={`A clustering based approach that will smooth out the transitions
              between all the different genres in your playlist by grouping them
              with similar songs.`}
            />
          </Paper>
        </Grid>
        <Grid sx={{ width: "25%" }} item>
          <Paper elevation={4}>
            <SimmeringCard
              name="Bake"
              image={baking_froggie}
              bgColor={"#B38D97"}
              textColor={"text.primary"}
              description={`A TSP-based approach that will organize your
              playlist based on finding the shortest musical path between your
              songs.`}
            />
          </Paper>
        </Grid>
        <Grid sx={{ width: "25%" }} item>
          <Paper elevation={4}>
            <SimmeringCard
              name="Microwave"
              image={microwaving_froggie}
              bgColor={"#422040"}
              textColor={"#ECBEB4"}
              description={`A chaotic method that we added just for fun - it
              will do its very best to make your playlist as transitionally
              unpleasant as possible.`}
            />
          </Paper>
        </Grid>
      </Grid>

      <Typography padding={4} variant="h4" align="center">
        To use these, please login to your Spotify account!
      </Typography>
    </Box>
  );
}

export default LoginFirst;
