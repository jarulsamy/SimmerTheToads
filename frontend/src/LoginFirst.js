import React from "react";
// import Box from "@mui/material/Box";
import { Container, Typography } from "@mui/material";
import { Box, Grid } from "@mui/material";
import Paper from "@mui/material/Paper";

// sx={{background: 'linear-gradient(to bottom, #F1DAC4, #ECBEB4)', width: '100%', height: '100%'}}

function LoginFirst() {
    return (
        <Container >
            <Typography variant="h1">Hi! Welcome to our website</Typography>
            <Typography variant="h3">We are Simmer The Toads. A spotify extention that aims to ...</Typography>
            <Typography padding={4} variant="h5">We developed three algorithms that will organize your playlists:</Typography>

            <Grid container justifyContent="space-evenly">
                <Grid sx={{width: '25%'}} item justifyContent={'center'}>
                    <Paper elevation={3} square>
                        <Box padding={3} color="text.secondary" bgcolor='#a3ac88'>
                            <Typography variant="h4">Simmer</Typography>
                            <Typography variant="body2">
                                A clustering based approach that will smooth out the transitions between all the different genres in your playlist
                            </Typography>
                        </Box>
                    </Paper>
                </Grid>
                <Grid sx={{width: '25%'}} item>
                    <Paper elevation={3}>
                        <Box padding={3} color="text.primary" bgcolor='#B38D97'>
                            <Typography variant="h4">Bake</Typography>
                            <Typography variant="body2">
                                A tsp based approach that will smooth out the transitions between all the different genres in your playlist
                            </Typography>
                        </Box>
                    </Paper>
                </Grid>
                <Grid sx={{width: '25%'}} item>
                    <Paper elevation={3}>
                        <Box padding={3} color="#ECBEB4" bgcolor='#422040'>
                            <Typography variant="h4">Microwave</Typography>
                            <Typography variant="body2">A chaos method that will do its very best to make your playlist as jerky and unpleasant as possible</Typography>
                        </Box>
                    </Paper>
                </Grid>
            </Grid>
            <Typography padding={4} variant="h5">To use these please login to your Spotify account!</Typography>
        </Container>
    )
}

export default LoginFirst;