import axios from "axios";

// Helper exception
class NotImplemented extends Error {
  constructor(message = "", ...args) {
    this.message = `${message}: Not yet implemented`;
  }
}

export default class APIService {
  // Use a single axios session for all the API transactions.
  // This way we preserve the session token.
  static axiosInstance = axios.create({
    withCredentials: true,
    baseURL: "/api/",
  });

  static getPlaylists() {
    return this.axiosInstance.get("playlists");
  }

  static getPlaylistTracks(playlist_id) {
    return this.axiosInstance.get(`playlist/${playlist_id}/tracks`);
  }

  static simmeredPlaylistTracks(playlist_id, to_spotify = false) {
    return this.axiosInstance.get(`simmered_playlist/${playlist_id}/tracks`, {
      params: {
        to_spotify: to_spotify,
      },
    });
  }
}
