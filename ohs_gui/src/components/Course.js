import React, { Component } from 'react';

class Course extends Component {
  render() {
    return (
      <div>Course: {this.props.match && this.props.match.params.id}</div>
    );
  }
}

export default Course;
