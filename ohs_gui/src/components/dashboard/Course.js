import React, { Component } from 'react';

class Course extends Component {
  render() {
    return (
      <div className="course card-element">
        {this.props.course.name}
      </div>
    );
  }
}

export default Course;
