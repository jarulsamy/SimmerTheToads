import "./css/Header.css";
import logo from "./images/froggie.png"
import React from "react";
import Box from "@mui/material/Box";
import { Typography } from "@mui/material";

function Header() {
    return (
        <React.Fragment>
            <Box sx={{ width: "100%", bgcolor: "#8D9575" }}>
                <Box component="img" src={logo} alt="Logo" className="logo"/>
                <Typography variant="h3">Simmer the Toads</Typography>
            </Box>
        </React.Fragment>
    )
}

export default Header;