import React from "react";
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import About from "./About";
import SongForm from "./song_form";
import Flask from "./Flask";
import "./Tabs.css";

function CreateTabs() {
    return (
        <Tabs className={"Tabs"}>
                <TabList className={"TabList"}>
                    <Tab className={"Tab"}>Create Playlist</Tab>
                    <Tab className={"Tab"}>Spotify</Tab>
                    <Tab className={"Tab"}>About</Tab>
                </TabList>


            <TabPanel className={"TabPanel"}>
                <SongForm />
            </TabPanel>
            <TabPanel className={"TabPanel"}>
                <h1>Spotify related things...</h1>
                <Flask />
            </TabPanel>
            <TabPanel className={"TabPanel"}>
                <About />
            </TabPanel>
        </Tabs>
    );
}

export default CreateTabs;