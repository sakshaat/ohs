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
        name: "CSC302",
        id: 1
      }, {
        name: "CSC309",
        id: 2
      }, {
        name: "CSC367",
        id: 3
      }, {
        name: "CSC258",
        id: 4
      }, {
        name: "CSC384",
        id: 5
      }
    ]
    this.setState({ courses: courses })
  }

  getSections() {
    // TODO: dummy json
    const sections = [
      {
        courseCode: "CSC302H1S",
        id: 6
      }, {
        courseCode: "CSC309H1S",
        id: 7
      }, {
        courseCode: "CSC367H1S",
        id: 8
      }, {
        courseCode: "CSC258H1S",
        id: 9
      }, {
        courseCode: "CSC384H1S",
        id: 10
      }
    ]
    this.setState({ sections: sections });
  }

  render() {
    const { courses, sections } = this.state;
    const isProf = this.props.user && this.props.user.role === "PROFESSOR";

    const studentView = (
      <div id="sections">
        <h2>Current Courses</h2>
        {sections.map(s => (
          <LectureSectionCard section={s} key={s.id} />
        ))}
      </div>
    );

    const profView = (
      <div id="courses">
        <h2>Current Courses</h2>
        {courses.map(c => (
          <CourseCard course={c} key={c.id} />
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
