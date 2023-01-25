"use strict";

// import React from "react";
// import ReactDOM from "react-dom/client";

const e = React.createElement;

class SongForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      song: '',
      songList: []
    };
    this.songState = ["init"];

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({song: event.target.value});
  }

  handleSubmit(event) {
    try {
      const aSong = this.state["song"];
      const songListTmp = this.state["songList"];
      console.log("songList before: " + songListTmp);
      songListTmp.push(aSong);
      console.log("songList after: " + songListTmp);
      this.setState({song: '', songList: songListTmp});
      event.preventDefault();
    }
    catch (err) {
      alert(err);
    }
  }

  render() {
    return (
      e(
        "form", 
        {onSubmit: this.handleSubmit}, 
        // {onSubmit: () => {this.handleSubmit, this.handleChange}}, 
        "Enter a song here: ",
        e('input', {type:'text', value: this.state.song, onChange: this.handleChange}),
        e('input', {type:'submit', value:'Submit'}),
        e('h1',null,'You have submitted '+this.state["songList"].length+' songs:'),
        e('ul',null,this.state["songList"].map((myList) => { return e('li',null,myList)}))
      )
    );
  }
  
}

const domContainer = document.querySelector("#songs");
const root = ReactDOM.createRoot(domContainer);
root.render(e(SongForm));
