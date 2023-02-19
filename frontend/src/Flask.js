import React, { Component } from "react";
import axios from "axios";

export class Spotify extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isAuthenticated: localStorage.getItem("isAuthenticated"),
      playlists: [],
    };
    this.axiosInstance = axios.create({
      withCredentials: true,
      baseURL: "/api/",
    });
  }

  componentDidMount() {
    // Restore the playlists if we are already logged in
    if (!this.state["isAuthenticated"]) {
      return;
    }

    this.populatePlaylists();
  }

  populatePlaylists() {
    this.axiosInstance
      .get("playlists", { withCredentials: true })
      .then((resp) => this.setState({ playlists: resp.data.items }));
  }

  login() {
    if (this.state["isAuthenticated"]) {
      // Already logged in
      return;
    }

    this.axiosInstance.post("login").then((resp) => {
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
          this.setState({ isAuthenticated: true });
          localStorage.setItem("isAuthenticated", "true");
          this.populatePlaylists();
        }
      }, 500);
    });
  }

  render() {
    if (!this.state["isAuthenticated"]) {
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
      <ul>
        {(this.state.playlists || []).map((i) => (
          <li key={i.id}>{i.name}</li>
        ))}
      </ul>
    );
  }
}

// TODO: This can probably be consolidated with the 'Spotify' component...
export class Flask extends Component {
  constructor(props) {
    super(props);
    this.state = { data: {} };
  }

  // Demo fetch from flask
  componentDidMount() {
    fetch("/api/")
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ data: result.message });
        },
        (error) => {
          this.setState({ data: error });
        }
      );
  }

  render() {
    return (
      <div>
        <pre>{JSON.stringify(this.state["data"])}</pre>
        <Spotify />
      </div>
    );
  }
}

export default Flask;
