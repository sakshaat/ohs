import React, { Component } from 'react';

class Meeting extends Component {
  render() {
    return (
      <div>Meeting: {this.props.match && this.props.match.params.id}</div>
    );
  }
}

export default Meeting;
