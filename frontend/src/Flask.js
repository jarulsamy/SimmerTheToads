import APIService from "./API_service";
import React, { Component } from "react";
import { APIContext } from "./API_service";

const initialState = {
  playlists: [],
};

export default class Spotify extends Component {
  static contextType = APIContext;
  state = { ...initialState };

  setDefaultState() {
    this.setState({ ...initialState });
  }

  componentDidMount() {
    // Restore the playlists if we are already logged in
    APIService.isLoggedIn().then((resp) => {
      this.context.setLoggedIn(resp.data.logged_in);
      this.populatePlaylists();
    });
  }

  populatePlaylists() {
    if (this.context.loggedIn) {
      APIService.getPlaylists().then((resp) => {
        this.setState({ ...this.state, playlists: resp.data.items });
      });
    }
  }

  login() {
    if (this.context.loggedIn) {
      // Already logged in
      return;
    }

    APIService.login().then((resp) => {
      const auth_url = resp.data.auth_url;

      // TODO: Sizing this might be important...
      // TODO: There is probably some error handling that needs to go on here...
      let login_win = window.open(
        auth_url,
        "Login",
        "popup=1,toolbar=0,status=0,width=548,height=650,modal=yes,alwaysRaised=yes"
      );

      let id = setInterval(() => {
        if (login_win.closed) {
          clearInterval(id);

          APIService.isLoggedIn().then((r) => {
            this.context.setLoggedIn(r.data.logged_in);
            this.populatePlaylists();
            window.location.reload();
          });
        }
      }, 500);
    });
  }

  logout() {
    if (!this.context.loggedIn) {
      return;
    }

    APIService.logout().then((resp) => {
      this.context.setLoggedIn(false);
      this.setDefaultState();
      window.location.href = resp.request.responseURL;
    });
  }

  render() {
    if (!this.context.loggedIn) {
      // Show the login URL if not logged in.
      return (
        <div>
          <button
            className="App-link"
            href="#"
            onClick={this.login.bind(this)}
            rel="noopener noreferrer"
          >
            Login with Spotify
          </button>
        </div>
      );
    }

    // Otherwise, list all the playlists of the current user.
    return (
      <div>
        <ul>
          {(this.state.playlists || []).map((i) => (
            <li key={i.id}>{i.name}</li>
          ))}
        </ul>
        <button
          className="App-link"
          href="#"
          onClick={this.logout.bind(this)}
          rel="noopener noreferrer"
        >
          Logout
        </button>
      </div>
    );
  }
}
