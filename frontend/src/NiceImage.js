// This component is intended to show an image nicely. React is cruel, and not a fan of image styling. This attempts to do so well.

import React from "react";
//import { styled } from '@mui/material/styles';
import Card from "@mui/material/Card";
import CardMedia from "@mui/material/CardMedia";
import logo from "./images/froggie.png";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";

export default function Person({ image = logo }) {
  console.log(image);
  return (
    // sx = {{ maxWidth:  350}}
    <Card>
      <Paper elevation={0}>
        <Box t={2}>
          <CardMedia
            component="img"
            height="400"
            width="400"
            image={image}
            alt="image is supposed to go here, we think."
            sx={{ objectFit: "contain" }}
          />
        </Box>
      </Paper>
    </Card>
  );
}
