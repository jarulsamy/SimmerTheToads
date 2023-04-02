import React, { Component } from "react";
import PlaylistCards from "./PlaylistsView";
import { APIContext } from "./API_service";

export default class Home extends Component {
  static contextType = APIContext;

  render() {
    if (!this.context.loggedIn) {
      return <div>Login first</div>;
    }

    return (
      <div>
        <PlaylistCards />
      </div>
    );
  }
}
