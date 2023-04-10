// This component is intended to show an individual.


import React from 'react';
//import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import logo from "./images/froggie.png"
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

export default function Person({ name = "Froggie",
    image = logo,
    description = "Froggie has been invaluable in motivating us. Without him we do not know how we would have finished." }) {
    console.log(name);
    return (
        // sx = {{ maxWidth:  350}}
        <Card variant="outlined">
            <Grid container spacing={0}>
                <Grid item xs={0} />
                <Grid item xs={6}>
                    <Paper elevation={0} >
                        <Box t={2} >
                            <CardMedia
                                component="img"
                                height="150"
                                width="150"
                                image={image}
                                // frontend/src/images/froggie.png
                                alt="image of the person"
                                sx={{ borderRadius: '10%' }}
                            />
                        </Box>
                    </ Paper>
                </Grid>
                <Grid item xs={3}>
                    <CardHeader title={name} />
                </Grid>
            </Grid>


            <CardContent>
                <Typography variant="body3" color="text.secondary">
                    {description}
                </Typography>
            </CardContent>

        </Card>
    );
}