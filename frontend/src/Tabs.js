// import "./css/Tabs.css";
import React , { useState } from "react";
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import About from "./About";
import PlaylistCards from "./PlaylistsView";
import SongForm from "./song_form";
import Spotify from "./Flask";

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 4 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

export default function CreateTabs() {
  const [value, setValue] = useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
          <Tab label="Create Playlist" {...a11yProps(0)} />
          <Tab label="Spotify" {...a11yProps(1)} />
          <Tab label="About" {...a11yProps(2)} />
          <Tab label="Simmer Existing Playlist" {...a11yProps(3)} />
        </Tabs>
      </Box>
      <TabPanel value={value} index={0}>
        <SongForm />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <h1>Spotify related things...</h1>
        <Spotify />
      </TabPanel>
      <TabPanel value={value} index={2}>
        <About />
      </TabPanel>
      <TabPanel value={value} index={3}>
        <PlaylistCards />
      </TabPanel>
    </Box>
  );
}