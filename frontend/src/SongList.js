import React from "react";
import "./css/SongList.css";

export default class SongList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      songs: isNaN(props.songList) ? [] : props.songList,
    };
    this.makeList = this.makeList.bind(this);
  }

  splitSongAndArtist(song) {
    var tmp = song.split(" by ");
    if (tmp.length > 1) {
      return { song: tmp[0], artist: tmp[1] };
    } else {
      return { song: tmp[0], artist: "" };
    }
  }

  makeList() {
    var table = [];
    var index = 0;
    this.state.songs.forEach((element) => {
      const splited = this.splitSongAndArtist(element);
      var row = (
        <tr key={index}>
          <td> {splited.song} </td>
          <td> {splited.artist} </td>
        </tr>
      );
      table.push(row);
      index += 1;
    });
    return table;
  }

  render() {
    return (
      <table>
        <tbody>
          <tr>
            <th>Song Name</th>
            <th>Artist</th>
          </tr>
          {this.makeList()}
        </tbody>
      </table>
    );
  }
}
