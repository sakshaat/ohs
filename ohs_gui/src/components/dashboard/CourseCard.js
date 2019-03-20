import React, { Component } from 'react';
import { Link } from 'react-router-dom'

class CourseCard extends Component {
  render() {
    return (
      <Link to={`/course/${this.props.course.course_code}`}>
        <div className="course card-element">
          {this.props.course.course_code}
        </div>
      </Link>
    );
  }
}

export default CourseCard;
