import "./css/App.css";
import CreateTabs from "./Tabs";
import Header from "./Header";
import { APIContextProvider } from "./API_service";
import { AlertPopup } from "./Alert";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Box } from "@mui/material";

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
  shape: {
    borderRadius: 20
  }
});


function App() {
  return (
    <div className="App">
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
  );
}

export default App;
