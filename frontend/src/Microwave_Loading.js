import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import Button from "@mui/material/Button";
import microwaving_froggie from "./images/loading_microwaving.gif"
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
          src={microwaving_froggie}
          style={{ width: "auto", height: "auto" }}
          alt="frog microwave"
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