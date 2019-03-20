import React, { Component } from 'react';
import CourseCard from "./dashboard/CourseCard"
import LectureSectionCard from "./dashboard/LectureSectionCard"
import { Link } from 'react-router-dom'

import "./Home.css"


class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courses: [],
      sections: []
    }

    this.getCourses = this.getCourses.bind(this);
    this.getSections = this.getSections.bind(this);
  }

  componentDidMount() {
    if (this.props.user && this.props.user.role === "PROFESSOR") {
      this.getCourses();
    }
    else {
      this.getSections();
    }
  }

  getCourses() {
    // TODO: dummy json
    const courses = [
      {
        course_code: "CSC302"
      }, {
        course_code: "CSC309"
      }, {
        course_code: "CSC367"
      }, {
        course_code: "CSC258"
      }, {
        course_code: "CSC384"
      }
    ]
    this.setState({ courses: courses })
  }

  getSections() {
    // TODO: dummy json
    const sections = [
      {
        course: "CSC302"
      }, {
        course: "CSC309"
      }, {
        course: "CSC367"
      }, {
        course: "CSC258"
      }, {
        course: "CSC384"
      }
    ]
    this.setState({ sections: sections });
  }

  render() {
    const { courses, sections } = this.state;
    const isProf = this.props.user && this.props.user.role === "PROFESSOR";

    const studentView = (
      <div id="sections">
        <h1>Current Courses</h1>
        {sections.map(s => (
          <LectureSectionCard section={s} key={s.course} />
        ))}
      </div>
    );

    const profView = (
      <div id="courses">
        <h1>Current Courses</h1>
        {courses.map(c => (
          <CourseCard course={c} key={c.course_code} />
        ))}
        <Link to={'/addCourse'}>
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
