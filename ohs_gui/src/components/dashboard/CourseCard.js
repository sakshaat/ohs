import React, { PureComponent } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

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

CourseCard.propTypes = {
  course: PropTypes.string.isRequired
};

export default CourseCard;
