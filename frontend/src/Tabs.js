import "./css/Tabs.css";
import About from "./About";
import PlaylistCards from "./PlaylistsView";
import React from "react";
import SongForm from "./song_form";
import Spotify from "./Flask";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";

function CreateTabs() {
  return (
    <Tabs className={"Tabs"}>
      <TabList className={"TabList"}>
        <Tab className={"Tab"}>Create Playlist</Tab>
        <Tab className={"Tab"}>Spotify</Tab>
        <Tab className={"Tab"}>About</Tab>
        <Tab className={"Tab"}>Simmer Existing Playlist</Tab>
      </TabList>

      <TabPanel className={"TabPanel"}>
        <SongForm />
      </TabPanel>
      <TabPanel className={"TabPanel"}>
        <h1>Spotify related things...</h1>
        <Spotify />
      </TabPanel>
      <TabPanel className={"TabPanel"}>
        <About />
      </TabPanel>
      <TabPanel className={"TabPanel"}>
        <PlaylistCards />
      </TabPanel>
    </Tabs>
  );
}

export default CreateTabs;
