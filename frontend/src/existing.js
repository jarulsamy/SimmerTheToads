import React from "react";
import APIService from "./API_service.js";
import "./css/SongForm.css";
import axios from "axios";

class ExistingPlaylist extends React.Component {
  state = { selected_playlist_id: null, playlists: [] };

  constructor(props) {
    super(props);
  }

  componentDidMount() {
    APIService.getPlaylists().then((res) => {
      const playlists = res.data.items;
      this.setState((oldState) => {
        return (oldState.playlists = playlists);
      });
    });

    APIService.getPlaylistID().then((res) => {
      const id = res.data.playlist_id;
      this.setState((oldState) => {
        return (oldState.selected_playlist_id = id);
      });
    });
  }

  render() {
    console.log(this.state.selected_playlist_id);
    return (
      <ul>
        {this.state.playlists.map((i) => (
          <li key={i.id}>
            <img src={i.images[0].url} onClick={() => APIService.setPlaylistID(i.id)}/>
            {i.name}
          </li>
        ))}
      </ul>
    );
  }
}

export default ExistingPlaylist;
