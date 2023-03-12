import * as React from "react";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import APIService from "./API_service";
import { Container } from "@mui/system";
import {
  Alert,
  AlertTitle,
  CardActionArea,
  Grid,
  Snackbar,
} from "@mui/material";

function PlaylistCard({ id, name, description, images, songs = [] }) {
  const image = images[0] || { url: "", height: 300, width: 300 };
  const [simmeredAlert, setSimmeredAlert] = React.useState(null);

  async function simmerPlaylist(playlist_id) {
    const resp = await APIService.simmeredPlaylistTracks(playlist_id, true);
    console.log(`Simmered: ${playlist_id}`);
    // console.log(resp);
    // setSimmeredAlert(
    //   <Alert severity="success">
    //     <AlertTitle>Success</AlertTitle>"Successfully simmered!"
    //   </Alert>
    // );
  }

  return (
    <Card sx={{ width: 300 }} variant="outlined">
      <CardActionArea onClick={() => console.log("TODO: Show a dialog here!")}>
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
      <CardActions>
        <Button size="small" onClick={() => simmerPlaylist(id)}>
          Simmer
          {simmeredAlert}
        </Button>
      </CardActions>
    </Card>
  );
}

class PlaylistCards extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      playlists: [],
    };
  }

  componentDidMount() {
    APIService.getPlaylists().then((resp) => {
      this.setState({ playlists: resp.data.items });
    });
  }

  render() {
    return (
      <Container>
        <Grid container spacing={4} justifyContent="center">
          {this.state.playlists.map((p) => {
            return (
              <Grid item key={p.id}>
                <Paper elevation={3}>
                  <PlaylistCard
                    id={p.id}
                    name={p.name}
                    description={p.description}
                    images={p.images}
                  />
                </Paper>
              </Grid>
            );
          })}
        </Grid>
      </Container>
    );
  }
}

export default PlaylistCards;
