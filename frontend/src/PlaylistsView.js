import * as React from "react";
import Paper from "@mui/material/Paper";
import { Box, Grid } from "@mui/material";
import APIService from "./API_service";
import { Container } from "@mui/system";
import { useAlert } from "./Alert";
import PlaylistCard from "./PlaylistCard";
import SimmerMenu from "./Menu";
import SimpleBackdrop from "./Loading";

const cardsStyles = {
  // backgroundColor: ,
  // width: ,
  height: "80vh",
  overflowY: 'scroll'
}

class PlaylistCards extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      playlists: [],
      toBeSimmered: [],
      simmerQueued: false,
      loading: false
    };

    this.simmerPlaylist = this.simmerPlaylist.bind(this);
    this.selectedCard = this.selectedCard.bind(this);
  }

  componentDidMount() {
    APIService.getPlaylists().then((resp) => {
      this.setState({ playlists: resp.data.items });
    });
  }

  selectedCard(isNew, newID, newName) {
    if (isNew) {
      console.log("adding to the list: "+newName)
      this.setState(prevState => ({
        toBeSimmered: [...prevState.toBeSimmered, {id: newID, name: newName}]
      }))
    }
    else {
      console.log("removing from the list: "+newName);
      var temp = this.state.toBeSimmered;
      var index = temp.indexOf({id: newID, name: newName});
      temp.splice(index, 1);
      this.setState({toBeSimmered: temp});
    }
  }

  simmerPlaylist(simmerMethod) {
    // this function is called when the user clicked one of the options in the dropdown menu
    if (this.state.toBeSimmered.length > 0) {
      // which simmering method
      var evaluator = (simmerMethod === "Simmer") ? "clustering" : ((simmerMethod === "Bake") ? "tsp" : "chaos");
      console.log("Simmering with method: "+evaluator);
      this.setState({loading: true});
      this.state.toBeSimmered.forEach(playlist => {
        console.log("playlsit id: "+playlist.id+", playlist name: "+playlist.name)
        this.setState({setSimmerQueued: true});
        // setAlert("info", `Started simmering ${playlist.name}. Please wait...`);
        APIService.simmeredPlaylistTracks(playlist.id, true, evaluator).then(
          (resp) => {
            console.log(`Simmered: ${playlist.id}`);
            // setAlert("success", `Successfully simmered: ${playlist.name}`);
            this.setState({setSimmerQueued: false});
            this.setState({loading: false});
          },
          (error) => {
            console.error(error);
            // setAlert("error", "Something went wrong. Please try again.");
            this.setState({setSimmerQueued: false});
            this.setState({loading: false});
          }
        );
      })
    }
    else {console.log("no playlists to simmer")}
  }

  render() {
    return (
      <Container>
        <Box sx={cardsStyles}>
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
                      selectedCard={this.selectedCard}
                    />
                  </Paper>
                </Grid>
              );
            })}
          </Grid>
        </Box>
        <Box 
          m={1}
          //margin
          display="flex"
          justifyContent="flex-end"
          alignItems="flex-end">
            <SimmerMenu onChange={this.simmerPlaylist}/>
        </Box>
        {this.state.loading ? <SimpleBackdrop /> : <></>}
      </Container>
    );
  }
}

export default PlaylistCards;


