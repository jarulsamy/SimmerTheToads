import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import { Dialog, Typography, DialogTitle } from "@mui/material";

export default function SimpleBackdrop(props) {
  const { animation } = props;
  const [open] = React.useState(true);
  return (
    <div>
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={open}
      >
        <Dialog open={true}>
          <img
            src={animation}
            style={{ width: "auto", height: "auto" }}
            alt="frog in pot"
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
