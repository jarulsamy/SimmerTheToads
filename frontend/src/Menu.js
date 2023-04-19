import * as React from "react";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { Box } from "@mui/material";

export default function SimmerMenu(props) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
    //do the thing to the playlist with the specific id
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box sx={{ zIndex: 100 }}>
      <Button
        id="basic-button"
        aria-controls={open ? "basic-menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open ? "true" : undefined}
        onClick={handleClick}
      >
        Simmer
      </Button>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          "aria-labelledby": "basic-button",
        }}
        anchorOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
        transformOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
      >
        <MenuItem onClick={(e) => props.onChange(e.target.innerText)}>
          Simmer
        </MenuItem>
        <MenuItem onClick={(e) => props.onChange(e.target.innerText)}>
          Bake
        </MenuItem>
        <MenuItem onClick={(e) => props.onChange(e.target.innerText)}>
          Microwave
        </MenuItem>
      </Menu>
    </Box>
  );
}
