import React, { Component } from 'react';
import { Link } from 'react-router-dom'

class CourseCard extends Component {
  render() {
    return (
      <Link to={`/course/${this.props.course}`}>
        <div className="course card-element">
          {this.props.course}
        </div>
      </Link>
    );
  }
}

export default CourseCard;
