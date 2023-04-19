import React, { Component } from "react";
import PlaylistCards from "./PlaylistsView";
import { APIContext } from "./API_service";
import PlaylistCardsContainer from "./PlaylistsView";
import LoginFirst from "./LoginFirst";

export default class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedPlaylist: "",
    };

    this.setSelectedPlaylist = this.setSelectedPlaylist.bind(this);
  }

  static contextType = APIContext;

  setSelectedPlaylist(id) {
    this.setState({ selectedPlaylist: id });
  }

  render() {
    if (!this.context.loggedIn) {
      return <LoginFirst />;
    }

    return <PlaylistCardsContainer />;
  }
}
