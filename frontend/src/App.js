import "./css/App.css";
import CreateTabs from "./Tabs";
import Header from "./Header";
import { APIContextProvider } from "./API_service";
import { AlertPopup } from "./Alert";

function App() {
  return (
    <div className="App">
      <APIContextProvider>
        <AlertPopup />
        <Header />
        <CreateTabs />
      </APIContextProvider>
    </div>
  );
}

export default App;
