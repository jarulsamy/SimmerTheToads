import React, { Component, useState } from "react";
import axios from "axios";

export class Spotify extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isAuthenticated: localStorage.getItem("isAuthenticated"),
    };
    this.axiosInstance = axios.create({
      withCredentials: true,
      baseURL: "/api/",
    });
  }

  componentDidMount() {
    // Do nothing on init.
  }

  login() {
    const { isAuthenticated } = this.state;
    if (this.isAuthenticated) {
      return;
    }

    this.axiosInstance.post("login").then((resp) => {
      const auth_url = resp.data.auth_url;
      window.location.replace(auth_url);

      // TODO: Sizing this might be important...
      // TODO: There is probably some error handling that needs to go on here...
      // let login_win = window.open(
      //   auth_url,
      //   "Login",
      //   "popup=1,toolbar=0,status=0,width=548,height=650,modal=yes,alwaysRaised=yes"
      // );

      // let id = setInterval(() => {
      //   if (login_win.closed) {
      //     clearInterval(id);
      //     this.setState({ isAuthenticated: true });
      //     console.log(resp.headers);
      //     const cookie = resp.headers["set-cookie"][0];
      //     this.axiosInstance.defaults.headers.Cookie = cookie;
      //   }
      // }, 500);
    });
  }

  render() {
    const { isAuthenticated } = this.state;
    if (!isAuthenticated) {
      return (
        <div>
          <a
            className="App-link"
            href="#"
            onClick={this.login.bind(this)}
            rel="noopener noreferrer"
          >
            Login with Spotify
          </a>
        </div>
      );
    }

    // Demo, fetch all the playlists
    const data = this.axiosInstance
      .get("playlists", { withCredentials: true })
      .then((resp) => {
        console.log(resp);
        return resp.data;
      });

    // .then((resp) => {
    //   console.log(resp.data);
    //   return <div>JSON.stringify(resp.data)</div>;
    // });

    return <div>Logout (Not implemented)</div>;
  }
}

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
    const { data, status } = this.state;
    return (
      <div>
        <pre>{JSON.stringify(data)}</pre>
        <Spotify />
      </div>
    );
  }
}

export default Flask;
