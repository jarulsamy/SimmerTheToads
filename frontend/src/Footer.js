import React from "react";
import footer_water from "./images/minibottom.png";
import Box from "@mui/material/Box";

function Footer() {
  return (
    <Box
      sx={{
        height: "150px",
        width: "100%",
        position: "fixed",
        bottom: 0,
        backgroundImage: `url(${footer_water})`,
        backgroundSize: "contain",
        backgroundAttachment: "fixed",
        backgroundPosition: "center bottom",
        backgroundRepeat: "no-repeat",
      }}
    ></Box>
  );
}
export default Footer;
