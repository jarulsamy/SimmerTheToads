import * as React from "react";
import Paper from "@mui/material/Paper";
import { Box, Grid } from "@mui/material";
import APIService from "./API_service";
import { Container } from "@mui/system";
import { useAlert } from "./Alert";
import bubble_stretched from "./images/long_lotus.png"
import celebratory_froggie from "./images/celebratory_froggie.png"
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
      simmerQueued: false,
      loading: false,
      loadingcomplete: false,
    };

    this.simmerPlaylist = this.simmerPlaylist.bind(this);
    this.selectedCard = this.selectedCard.bind(this);
  }

  selectedCard(isNew, newID, newName) {
    if (isNew) {
      console.log("adding to the list: " + newName);
      this.setState((prevState) => ({
        toBeSimmered: [...prevState.toBeSimmered, { id: newID, name: newName }],
      }));
    } else {
      console.log("removing from the list: " + newName);
      var temp = this.state.toBeSimmered;
      var index = temp.indexOf({ id: newID, name: newName });
      temp.splice(index, 1);
      this.setState({ toBeSimmered: temp });
    }
  }

  simmerPlaylist(simmerMethod) {
    // this function is called when the user clicked one of the options in the dropdown menu
    if (this.state.toBeSimmered.length > 0) {
      // which simmering method
      var evaluator =
        simmerMethod === "Simmer"
          ? "clustering"
          : simmerMethod === "Bake"
          ? "tsp"
          : "chaos";
      console.log("Simmering with method: " + evaluator);
      this.setState({ loading: true });
      this.state.toBeSimmered.forEach((playlist) => {
        console.log(
          "playlsit id: " + playlist.id + ", playlist name: " + playlist.name
        );
        this.setState({ setSimmerQueued: true });
        // setAlert("info", `Started simmering ${playlist.name}. Please wait...`);
        APIService.simmeredPlaylistTracks(playlist.id, true, evaluator).then(
          (resp) => {
            console.log(`Simmered: ${playlist.id}`);
            // setAlert("success", `Successfully simmered: ${playlist.name}`);
            this.setState({ setSimmerQueued: false });
            this.setState({ loading: false });
            this.setState({loadingcomplete: true});
          },
          (error) => {
            console.error(error);
            // setAlert("error", "Something went wrong. Please try again.");
            this.setState({ setSimmerQueued: false });
            this.setState({ loading: false });
          }
        );
      });
    } else {
      console.log("no playlists to simmer");
    }
  }

  render() {
    return (
      <Container>
        <div style={{ overflowY: "scroll", height: "80vh" }}>
          <PlaylistCards selectedCard={this.selectedCard} />
        </div>
        <Box
          m={1}
          //margin
          display="flex"
          justifyContent="flex-end"
          alignItems="flex-end"
        >
        <footer style={{position: "fixed", zIndex: '99', bottom: 450, paddingTop: 20}}>
          <SimmerMenu onChange={this.simmerPlaylist} />
        </footer>       
        </Box>
        {this.state.loading ? <SimpleBackdrop /> : <></>}
        {/* {this.state.loadingcomplete ? 
          <Dialog
            open={true}
            // onClose={} should trigger dialogue to close?
            style={{width: '200px', marginLeft: '40%', marginTop: '40%', backgroundImage: `url(${celebratory_froggie})`, backgroundSize:"contain", backgroundRepeat: 'no-repeat'}}
          >
          <DialogTitle>
            {" "}
            <Typography variant="h4">Playlist simmered!</Typography>
          </DialogTitle>
          <DialogActions>
            <Button variant="contained" color= "#f8ebdf">Close</Button>
          </DialogActions>
        </Dialog> : <></>}  */}
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
      <Grid
        container
        rowSpacing={4}
        spacing={4}
        justifyContent="center"
        style={{ overflow: "auto" }}
      >
        {playlists.map((p) => {
          return (
            <Grid item key={p.id}>
              <Paper elevation={3}>
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
      <span>&nbsp;&nbsp;</span>
    </Box>
  );
}

export default PlaylistCardsContainer;
