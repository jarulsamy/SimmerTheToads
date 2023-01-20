"use strict";

const e = React.createElement;

class HelloButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { show: false };
  }

  render() {
    if (this.state.show) {
      return "Hello, World!";
    }

    return e(
      "button",
      { onClick: () => this.setState({ show: true }) },
      "Click Me!"
    );
  }
}

const domContainer = document.querySelector("#hello_button_container");
const root = ReactDOM.createRoot(domContainer);
root.render(e(HelloButton));
