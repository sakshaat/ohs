import React, { PureComponent } from 'react';
import { Link } from 'react-router-dom';

class CourseCard extends PureComponent {
  render() {
    const { course } = this.props;
    return (
      <Link to={`/course/${course}`}>
        <div className="course card-element">{course}</div>
      </Link>
    );
  }
}

export default CourseCard;
