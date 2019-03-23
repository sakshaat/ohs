import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import shortid from 'shortid';

import CourseCard from './CourseCard';
import LectureSectionCard from './LectureSectionCard';
import './Dashboard.css';

class Dashboard extends Component {
  render() {
    const { user, sections, courses } = this.props;
    const isProf = user && user.role === 'PROFESSOR';
    const studentView = (
      <div id="sections">
        <h1>Current Courses</h1>
        {sections.map(s => (
          <LectureSectionCard section={s} key={shortid.generate()} />
        ))}
      </div>
    );

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

    return isProf ? profView : studentView;
  }
}

export default Dashboard;
