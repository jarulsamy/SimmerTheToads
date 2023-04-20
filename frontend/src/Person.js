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

export default function Person({
  name = "Froggie",
  image = logo,
  description = `Froggie has been invaluable in motivating us. Without him we do
  not know how we would have finished.`,
}) {
  return (
    <Paper elevation={4}>
      <Card variant="outlined">
        <Grid container spacing={0}>
          <Grid item xs={6}>
            <Box t={2}>
              <CardMedia
                component="img"
                height="150"
                width="150"
                image={image}
                alt="Image of Person"
                sx={{ borderRadius: "10%" }}
              />
            </Box>
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
    </Paper>
  );
}
