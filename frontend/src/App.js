import "./css/App.css";
import CreateTabs from "./Tabs";
import Header from "./Header";
import { APIContextProvider } from "./API_service";
import { AlertPopup } from "./Alert";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Box } from "@mui/material";
import froggie_bg from "./images/long_bg.png"

const theme = createTheme({
  palette: {
    primary: {
        // light: will be calculated from palette.primary.main,
        main: '#422040',
        // dark: will be calculated from palette.primary.main,
        contrastText: '#ECBEB4'
    },
    secondary: {
        // light: will be calculated from palette.secondary.main,
        main: '#414535',
        // dark: will be calculated from palette.secondary.main,
        contrastText: '#F1DAC4',
    },
    text: {
      primary: '#422040',
      secondary: '#414535',
      disabled: "#8D9575"
    }
  ,
  background: {
    paper: "#f8ebdf",
    default: "#f8ebdf"
  }
  },
  typography: {
    fontFamily: ["DynaPuff", "cursive"].join(","),
    h1: {
      fontFamily: ["DynaPuff", "cursive"].join(",")
    },
    h2: {
      fontFamily: ["DynaPuff", "cursive"].join(",")
    },
    h3: {
      fontFamily: ["DynaPuff", "cursive"].join(",")
    },
    h4: {
      fontFamily: ["DynaPuff", "cursive"].join(",")
    },
    body1: {
      fontFamily: ["Alata", "sans-serif"].join(",")
    },
    body2: {
      fontFamily: ["Alata", "sans-serif"].join(",")
    },
    body3: {
      fontFamily: ["Alata", "sans-serif"].join(",")
    }
  },
  shape: {
    borderRadius: 20
  },
});


function App() {
  return (
    <div className="App">
      <div style={
        { backgroundImage: `url(${froggie_bg})`, backgroundSize:"contain", backgroundAttachment: 'fixed', backgroundPosition: 'center bottom', backgroundColor: '#f3e3db'}
        }>
        <ThemeProvider theme={theme}>
          <APIContextProvider>
            <AlertPopup />
            <Box style={{position: "fixed", top: 0, width: '100%', zIndex: '99'}}>
              <Header />
            </Box>
            <div style={{marginTop: '56px'}}>
              <CreateTabs />
            </div>
          </APIContextProvider>
        </ThemeProvider>
      </div>
    </div>
  );
}

export default App;
