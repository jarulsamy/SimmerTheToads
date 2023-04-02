import React from "react";
import { Component } from "react";
import APIService, { APIContext } from "./API_service";
import { Button } from "@mui/material";
import Box from "@mui/material/Box";
import Avatar from "@mui/material/Avatar";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import IconButton from "@mui/material/IconButton";
import Logout from "@mui/icons-material/Logout";

class UserDropdown extends Component {
  logout() {
    APIService.logout().then((resp) => {
      window.location.href = resp.request.responseURL;
      window.location.reload();
    });
  }

  constructor() {
    super();
    this.state = { data: null };
  }

  componentDidMount() {
    this.setState({});
    APIService.getMe().then((resp) => {
      this.setState({ anchorEl: null, data: resp.data });
    });
  }

  render() {
    if (this.state === null || this.state.data === null) {
      // Wait for the API service exchanges to finish.
      return <></>;
    }

    const handleClick = (event) => {
      this.setState({ ...this.state, anchorEl: event.currentTarget });
    };
    const handleClose = () => {
      this.setState({ ...this.state, anchorEl: null });
    };

    const handleProfileClick = () => {
      window.open(this.state.data.external_urls.spotify);
      handleClose();
    };

    const handleLogoutClick = () => {
      this.logout();
    };

    // return <Button onClick={this.logout}>Logout</Button>;
    const anchorEl = this.state.anchorEl;
    const open = Boolean(anchorEl);
    // const avatarURL = this.state.
    const images = this.state.data.images ?? [{ url: undefined }];
    const avatarURL = images[0].url;

    return (
      <React.Fragment>
        <Box>
          <IconButton
            onClick={handleClick}
            size="small"
            sx={{ ml: 2 }}
            aria-controls={open ? "account-menu" : undefined}
            aria-haspopup="true"
            aria-expanded={open ? "true" : undefined}
          >
            <Avatar src={avatarURL} />
          </IconButton>
        </Box>
        <Menu
          anchorEl={anchorEl}
          id="account-menu"
          open={open}
          onClose={handleClose}
          onClick={handleClose}
          PaperProps={{
            elevation: 0,
            sx: {
              overflow: "visible",
              filter: "drop-shadow(0px 2px 8px rgba(0,0,0,0.32))",
              mt: 1.5,
              "& .MuiAvatar-root": {
                width: 32,
                height: 32,
                ml: -0.5,
                mr: 1,
              },
              "&:before": {
                content: '""',
                display: "block",
                position: "absolute",
                top: 0,
                right: 14,
                width: 10,
                height: 10,
                bgcolor: "background.paper",
                transform: "translateY(-50%) rotate(45deg)",
                zIndex: 0,
              },
            },
          }}
          transformOrigin={{ horizontal: "right", vertical: "top" }}
          anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
        >
          <MenuItem onClick={handleProfileClick}>
            <ListItemIcon>
              <img
                alt=""
                src={
                  // Totally didn't steal this from spotify...
                  // May need to change later depending on sizing needs.
                  "https://open.spotifycdn.com/cdn/images/favicon16.1c487bff.png"
                }
              ></img>
            </ListItemIcon>
            Profile
          </MenuItem>
          <MenuItem onClick={handleLogoutClick}>
            <ListItemIcon>
              <Logout />
            </ListItemIcon>
            Logout
          </MenuItem>
        </Menu>
      </React.Fragment>
    );
  }
}

export default class LoginButton extends Component {
  static contextType = APIContext;

  login() {
    const height = window.screen.height / 2;
    const width = window.screen.width / 3;
    const params = `scrollbars=no,status=no,location=no,toolbar=no,menubar=no,width=${width},height=${height}`;

    APIService.login().then((resp) => {
      const auth_url = resp.data.auth_url;
      let handle = window.open(auth_url, "Login", params);
      if (!handle) {
        // Popup blocker probably caught it.
      }

      let id = setInterval(() => {
        if (!handle.closed) {
          return;
        }
        handle.close();
        window.location.reload();
        clearInterval(id);
      }, 500);
    });
  }

  render() {
    if (!this.context.loggedIn) {
      return <Button onClick={this.login.bind(this)}>Login</Button>;
    }
    return <UserDropdown />;
  }
}
