"use strict";

// import React from "react";
// import ReactDOM from "react-dom/client";
import APIService from './API_service.js';


const e = React.createElement;

class SongForm extends React.Component {
  
  constructor(props) {
    super(props);
    this.state = {
      song: '',
      songList: []
    };
    this.songState = [""];
    this.handlers = {
      submit1: this.handle_submit_add_song,
      submit2: this.handle_submit_send_playlist,
    }
    
    
    this.submit_handler = this.submit_handler.bind(this);
    this.handle_submit_add_song = this.handle_submit_add_song.bind(this);
    this.handle_submit_send_playlist = this.handle_submit_send_playlist.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }
  
  handle_submit_send_playlist() {
    console.log("playlist to send: " + JSON.stringify(this.state["songList"]));
    APIService.sendPlaylist(this.state["songList"]);
    // .then((response) => props.insertedArticle(response))
    // .catch(error => console.log('error',error))
  }
  
  handle_submit_add_song(event) {
    try {
      // Song submitted
      const aSong = this.state["song"];
      // Current song list
      const songListTmp = this.state["songList"];
      // Add new song
      songListTmp.push(aSong);
      this.setState({song: '', songList: songListTmp});
      // Don't refresh the page
      event.preventDefault();
    }
    catch (err) {
      alert(err);
    }
  }

  submit_handler(e, id) {
    try {
      // Don't refresh the page
      e.preventDefault();
      
      if (id == "submit1") {
        this.handle_submit_add_song(e);
      }
      if (id == "submit2") {
        this.handle_submit_send_playlist(e);
      }
    }
    catch (err) {
      console.log(err);
    }

  };

  handleChange(event) {
    this.setState({song: event.target.value});
  }

  render() {
    return (
      e( "div", null,
        e(
          "form", 
          {id: "submit1", onSubmit: (e) => this.submit_handler(e, e.target.id)}, 
          "Enter a song here: ",
          e('input', {type:'text', value: this.state.song, onChange: this.handleChange}),
          e('input', {type:'submit', value:'Submit'}),
          e('h1',null,'You have submitted '+this.state["songList"].length+' songs:'),
          e('ul',null,this.state["songList"].map((myList) => { return e('li',{key: myList},myList)}))
        ),
        e('button', {id: "submit2", type:'submit', onClick: (e) => this.submit_handler(e, e.target.id)}, "Make me a playlist!")
      )
    );
  }
  
}

const domContainer = document.querySelector("#songs");
const root = ReactDOM.createRoot(domContainer);
root.render(e(SongForm));
