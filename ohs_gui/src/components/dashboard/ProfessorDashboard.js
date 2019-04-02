import React from 'react';
import shortid from 'shortid';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

import CourseCard from './CourseCard';
import './ProfessorDashboard.css';

class ProfessorDashboard extends React.Component {
  render() {
    const { courses } = this.props;
    console.log(courses);
    const profView = (
      <div id="courses">
        <h1>Current Courses</h1>
        {courses.map(c => (
          <CourseCard course={c} key={shortid.generate()} />
        ))}
        <Link to="/add-course">
          <div className="add-course card-element">
            <span className="fa fa-plus" />
          </div>
        </Link>
      </div>
    );

    return profView;
  }
}

ProfessorDashboard.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  courses: PropTypes.array.isRequired
};

export default ProfessorDashboard;
