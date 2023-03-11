import * as React from "react";
import Box from "@mui/material/Box";
import Collapse from "@mui/material/Collapse";
import IconButton from "@mui/material/IconButton";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import APIService from "./API_service";
import { Container } from "@mui/system";
import { Grid } from "@mui/material";

function PlaylistCard({ id, name, description, images }) {
  const image = images[0] || { url: "", height: 300, width: 300 };
  return (
    <Card sx={{ width: 300 }} variant="outlined">
      <CardMedia
        sx={{ height: 300 }}
        component="img"
        image={image.url}
        title={name}
      />
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small">TODO</Button>
      </CardActions>
    </Card>
  );
}

class PlaylistTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      playlists: [],
    };
  }

  componentDidMount() {
    APIService.getPlaylists().then((resp) => {
      this.setState({ playlists: resp.data.items });
    });
  }

  render() {
    return (
      <Container>
        <Grid container spacing={4} justifyContent="center">
          {this.state.playlists.map((p) => {
            return (
              <Grid item>
                <Paper elevation={3}>
                  <PlaylistCard
                    id={p.id}
                    name={p.name}
                    description={p.description}
                    images={p.images}
                  />
                </Paper>
              </Grid>
            );
          })}
        </Grid>
      </Container>
    );
  }
}

export default PlaylistTable;
