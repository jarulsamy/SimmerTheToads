"use strict";

const e = React.createElement;

class SongForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    alert('A song was submitted: ' + this.state.value);
    event.preventDefault();
  }

  render() {
    return (
      e(
        "form", 
        {onSubmit: () => {this.handleSubmit}}, 
        "Enter a song here: ",
        e('input', {type:'text', onChange:()=>{this.handleChange}}),
        e('input', {type:'submit'})
        )
    );
  }
}

const domContainer = document.querySelector("#songs");
const root = ReactDOM.createRoot(domContainer);
root.render(e(SongForm));
