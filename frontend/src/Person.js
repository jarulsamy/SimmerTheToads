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

export default function Person({name = "Froggie",
    image = logo,
    description = "Froggie has been invaluable in motivating us. Without him we do not know how we would have finished."}) {
    console.log(name);
        return (
        <Card sx={{ maxWidth: 345 }} variant="outlined"> 
            <CardHeader title= {name} />            
            <CardMedia
                component="img"
                height="194"
                image={image}
                // frontend/src/images/froggie.png
                alt="image of the person"
            />
            <CardContent>
                <Typography variant="body2" color="text.secondary">
                   {description}
                </Typography>
            </CardContent>

        </Card>
    );
}