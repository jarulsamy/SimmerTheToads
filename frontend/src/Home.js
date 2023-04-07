import React, { Component } from "react";
import PlaylistCards from "./PlaylistsView";
import { APIContext } from "./API_service";

export default class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedPlaylist: ''
    }

    this.setSelectedPlaylist = this.setSelectedPlaylist.bind(this);
  }

  static contextType = APIContext;

  setSelectedPlaylist(id) {
    this.setState({selectedPlaylist: id});
  }

  render() {
    if (!this.context.loggedIn) {
      return <div>Login first</div>;
    }

    return (
      <div>
        <PlaylistCards />
        {/* <SimmeringButton /> */}
      </div>
    );
  }
}
