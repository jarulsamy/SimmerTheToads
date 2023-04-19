import * as React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { CardActionArea } from "@mui/material";

export default function PlaylistCard({
  id,
  name,
  description,
  images,
  songs = [],
  selectedCard,
}) {
  const image = images[0] || { url: "", height: 300, width: 300 };
  const [simmerQueued, setSimmerQueued] = React.useState(false);
  const [bgColor, setBgColor] = React.useState("#f8ebdf");

  return (
    <Card
      style={{ height: "100%" }}
      sx={{ width: 300, bgcolor: bgColor }}
      variant="outlined"
    >
      <CardActionArea
        onClick={() => {
          selectedCard(!simmerQueued, id, name);
          !simmerQueued ? setBgColor("#ECBEB4") : setBgColor("#f8ebdf");
          simmerQueued ? setSimmerQueued(false) : setSimmerQueued(true);
        }}
      >
        <CardMedia
          sx={{ height: 300 }}
          component="img"
          image={image.url}
          title={name}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {description}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
}
