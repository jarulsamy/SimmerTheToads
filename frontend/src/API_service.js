import axios from "axios";
import React from "react";

// https://react.dev/learn/passing-data-deeply-with-context#use-cases-for-context

const initialState = {
  loggedIn: false,
};
export const APIContext = React.createContext(initialState);
export const APIContextProvider = ({ children }) => {
  const [loggedIn, setLoggedIn] = React.useState(false);

  APIService.isLoggedIn().then((resp) => {
    setLoggedIn(resp.data.logged_in);
  });

  return (
    <APIContext.Provider value={{ loggedIn, setLoggedIn }}>
      {children}
    </APIContext.Provider>
  );
};

export default class APIService {
  // Use a single axios session for all the API transactions.
  // This way we preserve the session token.
  static axiosInstance = axios.create({
    withCredentials: true,
    baseURL: "/api/",
  });

  static isLoggedIn() {
    return this.axiosInstance.get("login");
  }

  static login() {
    return this.axiosInstance.post("login");
  }

  static logout() {
    return this.axiosInstance.get("logout");
  }

  static getMe() {
    return this.axiosInstance.get("me");
  }

  static getPlaylists() {
    return this.axiosInstance.get("playlists");
  }

  static getPlaylistTracks(playlist_id) {
    return this.axiosInstance.get(`playlist/${playlist_id}/tracks`);
  }

  static simmeredPlaylistTracks(playlist_id, to_spotify = false, simmerMethod = "clustering") {
    return this.axiosInstance.get(`simmered_playlist/${playlist_id}/tracks`, {
      params: {
        to_spotify: to_spotify,
        evaluator: simmerMethod,
      },
    });
  }
}
