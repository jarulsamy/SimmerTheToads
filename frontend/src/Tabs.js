import React, { useState } from "react";
import PropTypes from "prop-types";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import About from "./About";
import LoginButton from "./Login";
import Home from "./Home";
import Header from "./Header";
import { Stack } from "@mui/system";
import { Container } from "@mui/material";
import Footer from "./Footer";

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
    "aria-controls": `simple-tabpanel-${index}`,
  };
}

export default function CreateTabs() {
  const [value, setValue] = useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box>
      <Stack>
        <Box sx={{ pb: 2, position: "sticky", top: 0, zIndex: 99 }}>
          <Header />
          <Tabs
            sx={{ bgcolor: "#ECBEB4" }}
            value={value}
            onChange={handleChange}
            aria-label="Tabs"
          >
            <Tab label="Home" {...a11yProps(0)} />
            <Tab label="About" {...a11yProps(1)} />
            <LoginButton />
          </Tabs>
        </Box>

        <Box>
          <TabPanel value={value} index={0}>
            <Home />
          </TabPanel>
        </Box>
        <Container>
          <TabPanel value={value} index={1}>
            <About />
          </TabPanel>
        </Container>
        <Box sx={{ pb: 2, position: "sticky", bottom: 0, zIndex: 99 }}>
          <Footer />
        </Box>
      </Stack>
    </Box>
  );
}
