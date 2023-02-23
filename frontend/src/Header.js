import "./Header.css";
import logo from "./images/froggie.png"
import React from "react";

function Header() {
    return (
        <div className="header">
            <img src={logo} alt="Logo" className="logo"/>
            <h1 className="title">Simmer the Toads</h1>
        </div>
    )
    // consider adding an onClick to return to home page when logo is clicked
}

export default Header;