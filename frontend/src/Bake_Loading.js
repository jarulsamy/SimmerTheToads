import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import Button from "@mui/material/Button";
import baking_froggie from "./images/baking_froggie.gif"
import {
  Dialog,
  DialogActions,
  Typography,
  DialogTitle,
} from "@mui/material";

export default function SimpleBackdrop() {
  const [open, setOpen] = React.useState(true);
  const handleClose = () => {
    setOpen(false);
  };
  const handleToggle = () => {
    setOpen(!open);
  };

  return (
    <div>
      {/* <Button onClick={handleToggle}>Show backdrop</Button> */}
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={open}
        onClick={handleClose}
      >
        <Dialog open={true}>
        <img
          src={baking_froggie}
          style={{ width: "auto", height: "auto" }}
          alt="frog baking"
        ></img>
          <DialogTitle>
            {" "}
            <Typography variant="h4">Simmering...</Typography>
          </DialogTitle>
        </Dialog>
      </Backdrop>
    </div>
  );
}