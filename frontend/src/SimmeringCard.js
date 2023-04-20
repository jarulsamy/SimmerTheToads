import React from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import logo from "./images/froggie.png";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";

export default function SimmeringCard({
  name = "Froggie",
  image = logo,
  bgColor = "#B38D97",
  textColor = "text.secondary",
  description = "Froggie has been invaluable in motivating us. Without him we do not know how we would have finished.",
}) {
  console.log(name);
  return (
    // sx = {{ maxWidth:  350}}
    <Card variant="outlined" sx={{backgroundColor: bgColor}}>
        <Box t={2} align="center">
              <CardMedia
                component="img"
                height="400"
                width="400"
                image={image}
                // frontend/src/images/froggie.png
                alt="image"
                sx={{ borderRadius: "10%", objectFit: "contain" }}
              />
            </Box>
      <CardHeader title={name} align="center" variant="h2" sx={{color: textColor}}/>
      <CardContent>
        <Typography variant="body3" align="center" sx={{color: textColor}}>
          {description}
        </Typography>
      </CardContent>
    </Card>
  );
}
