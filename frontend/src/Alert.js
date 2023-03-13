import * as React from "react";
import { Snackbar } from "@mui/material";
import { createContext, useContext, useState } from "react";
import MuiAlert from "@mui/material/Alert";

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const ALERT_TIMEOUT = 5000;
const initialState = {
  type: "",
  text: "",
};

const AlertContext = createContext({
  ...initialState,
  setAlert: () => {},
});

export const AlertProvider = ({ children }) => {
  const [text, setText] = useState("");
  const [type, setType] = useState("");

  const setAlert = (type, text) => {
    setType(type);
    setText(text);
  };

  return (
    <AlertContext.Provider value={{ text, type, setAlert }}>
      {children}
    </AlertContext.Provider>
  );
};

export const useAlert = () => useContext(AlertContext);

export default AlertContext;

export const AlertPopup = () => {
  const { setAlert, type, text } = useAlert();

  const onClose = () => {
    setAlert("", "");
  };

  if (text && type) {
    return (
      <Snackbar open={true} autoHideDuration={ALERT_TIMEOUT} onClose={onClose}>
        <Alert severity={type} sx={{ width: "100%" }}>
          {text}
        </Alert>
      </Snackbar>
    );
  }
  return <></>;
};
