// import logo from "./logo.svg";
import { AlertPopup } from "./Alert";
import "./css/App.css";
// import axios from "axios";
import Header from "./Header";
import CreateTabs from "./Tabs";

function App() {
  return (
    <div className="App">
      <AlertPopup />
      <Header />
      <CreateTabs />
    </div>
  );
}

export default App;
