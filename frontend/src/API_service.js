import axios from "axios";

export default class APIService {
  static axiosInstance = axios.create({
    withCredentials: true,
    baseURL: "/api/",
  });

  // Insert an article
  static sendPlaylist(body) {
    return fetch(`/playlist`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })
      .then((response) => response.json())
      .catch((error) => console.log(error));
  }

  static getPlaylists() {
    return this.axiosInstance.get("playlists");
  }

  static setPlaylistID(id) {
    return this.axiosInstance.put("playlist_id", { playlist_id: id });
  }

  static getPlaylistID() {
    return this.axiosInstance.get("playlist_id");
  }
}
