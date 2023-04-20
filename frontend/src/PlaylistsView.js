import * as React from "react";
import Paper from "@mui/material/Paper";
import { Box, Fab, Grid } from "@mui/material";
import APIService from "./API_service";
import { Container } from "@mui/system";
import celebratory_froggie from "./images/celebratory_froggie.png";
import headphone_froggie from "./images/headphone_froggie.png";
import sad_froggie from "./images/sad_froggie.png";
import loadingBake from "./images/loading_baking.gif";
import loadingSimmer from "./images/loading_simmer.gif";
import loadingMicrowave from "./images/loading_microwaving.gif";
import PlaylistCard from "./PlaylistCard";
import SimmerMenu from "./Menu";
import SimpleBackdrop from "./Loading";
import {
  Dialog,
  DialogActions,
  Typography,
  DialogTitle,
  Button,
} from "@mui/material";

class PlaylistCardsContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      toBeSimmered: [],
      loading: false,
      animationSrc: null,
      dialog: <></>,
    };

    this.simmerPlaylist = this.simmerPlaylist.bind(this);
    this.selectedCard = this.selectedCard.bind(this);
  }

  selectedCard(isNew, newID, newName) {
    if (isNew) {
      this.setState((prevState) => ({
        ...prevState,
        toBeSimmered: [...prevState.toBeSimmered, { id: newID, name: newName }],
      }));
    } else {
      var temp = this.state.toBeSimmered;
      var index = temp.indexOf({ id: newID, name: newName });
      temp.splice(index, 1);
      this.setState({ ...this.state, toBeSimmered: temp });
    }
  }

  simmerPlaylist(simmerMethod) {
    const handleDialogClose = () => {
      this.setState({ ...this.state, dialog: <></> });
    };

    const successDialog = (
      <Dialog open={true}>
        <img
          src={celebratory_froggie}
          style={{ width: "auto", height: "auto" }}
          alt="Celebratory Frog"
        ></img>
        <DialogTitle>
          {" "}
          <Typography variant="h4">Playlist simmered!</Typography>
        </DialogTitle>
        <DialogActions>
          <Button variant="contained" onClick={handleDialogClose}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    );

    const failureDialog = (
      <Dialog open={true}>
        <img
          src={sad_froggie}
          style={{ width: "auto", height: "auto" }}
          alt="sad frog"
        ></img>
        <DialogTitle>
          {" "}
          <Typography variant="h4">
            Oops, something went wrong. Playlist wasn't simmered...
          </Typography>
        </DialogTitle>
        <DialogActions>
          <Button variant="contained" onClick={handleDialogClose}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    );

    const noPlaylistsDialog = (
      <Dialog open={true}>
        <img
          src={headphone_froggie}
          style={{ width: "auto", height: "auto" }}
          alt="Headphone Frog"
        ></img>
        <DialogTitle>
          <Typography variant="h4">
            Please select at least one playlist to simmer.
          </Typography>
        </DialogTitle>
        <DialogActions>
          <Button variant="contained" onClick={handleDialogClose}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    );

    if (this.state.toBeSimmered.length <= 0) {
      this.setState({ ...this.state, dialog: noPlaylistsDialog });
      return;
    }

    let evaluator;
    let animationSrc;
    switch (simmerMethod) {
      case "Simmer":
        evaluator = "clustering";
        animationSrc = loadingSimmer;
        break;
      case "Bake":
        evaluator = "tsp";
        animationSrc = loadingBake;
        break;
      default:
        evaluator = "chaos";
        animationSrc = loadingMicrowave;
        break;
    }
    this.setState({ ...this.state, loading: true, animationSrc: animationSrc });

    this.state.toBeSimmered.forEach((playlist) => {
      APIService.simmeredPlaylistTracks(playlist.id, true, evaluator).then(
        (resp) => {
          this.setState({
            ...this.state,
            loading: false,
            dialog: successDialog,
          });
        },
        (error) => {
          console.error(error);
          this.setState({
            loading: false,
            dialog: failureDialog,
          });
        }
      );
    });
  }

  render() {
    let animation = this.state.animationSrc || loadingSimmer;

    return (
      <Container>
        <PlaylistCards selectedCard={this.selectedCard} />
        <Box
          display="flex"
          justifyContent="flex-end"
          alignItems="flex-end"
          sx={{ zIndex: 100 }}
        >
          <header
            style={{
              position: "fixed",
              bottom: 0,
              paddingBottom: 100,
              zIndex: 100,
            }}
          >
            <Fab
              variant="extended"
              size="large"
              sx={{ position: "sticky", zIndex: 101 }}
            >
              <SimmerMenu onChange={this.simmerPlaylist} />
            </Fab>
          </header>
        </Box>
        {this.state.loading ? <SimpleBackdrop animation={animation} /> : <></>}
        {this.state.dialog}
      </Container>
    );
  }
}

function PlaylistCards(props) {
  const [playlists, setPlaylists] = React.useState([]);

  React.useEffect(() => {
    APIService.getPlaylists().then((resp) => {
      setPlaylists(resp.data.items);
    });
  }, []);

  return (
    <Box>
      <Grid container rowSpacing={4} spacing={4} justifyContent="center">
        {playlists.map((p) => {
          return (
            <Grid item key={p.id}>
              <Paper elevation={4}>
                <PlaylistCard
                  id={p.id}
                  name={p.name}
                  description={p.description}
                  images={p.images}
                  selectedCard={props.selectedCard}
                />
              </Paper>
            </Grid>
          );
        })}
      </Grid>
    </Box>
  );
}

export default PlaylistCardsContainer;
