import logo from "./logo.svg";
import "./App.css";
import Flask from "./Flask";
import axios from "axios";
import React from "react";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Simmer the Toads, now with more JS!</p>
        <Flask />
      </header>
    </div>
  );
}

export default App;
