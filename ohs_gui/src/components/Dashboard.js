import React, { Component } from 'react';
import CourseCard from "./dashboard/CourseCard"
import LectureSectionCard from "./dashboard/LectureSectionCard"
import { Link } from 'react-router-dom'

import "./Home.css"
import shortid from 'shortid';

class Dashboard extends Component {
  render() {
    const isProf = this.props.user && this.props.user.role === "PROFESSOR";
    const studentView = (
      <div id="sections">
        <h1>Current Courses</h1>
        {this.props.sections.map(s => (
          <LectureSectionCard section={s} key={shortid.generate()} />
        ))}
      </div>
    );

    const profView = (
      <div id="courses">
        <h1>Current Courses</h1>
        {this.props.courses.map(c => (
          <CourseCard course={c} key={shortid.generate()} />
        ))}
        <Link to={'/add-course'}>
          <div className="add-course card-element">
            <span className="fa fa-plus"></span>
          </div>
        </Link>
      </div>
    );

    return isProf ? profView : studentView;
  }
}

export default Dashboard;
