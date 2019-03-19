import React, { Component } from 'react';
import Course from "./dashboard/Course"
import LectureSection from "./dashboard/LectureSection"
import Meeting from "./dashboard/Meeting"

import "./Home.css"


class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courses: [],
      sections: [],
      meetings: []
    }

    this.getCourses = this.getCourses.bind(this);
    this.getSections = this.getSections.bind(this);
    this.getMeetings = this.getMeetings.bind(this);
  }

  componentDidMount() {
    if (this.props.user && this.props.user.role === "PROFESSOR") {
      this.getCourses();
    }
    else {
      this.getSections();
    }
    this.getMeetings();
  }

  getCourses() {
    // TODO: dummy json
    const courses = [
      {
        name: "CSC302"
      }, {
        name: "CSC309"
      }, {
        name: "CSC367"
      }, {
        name: "CSC258"
      }, {
        name: "CSC384"
      }
    ]
    this.setState({ courses: courses })
  }

  getSections() {
    // TODO: dummy json
    const sections = [
      {
        courseCode: "CSC302H1S"
      }, {
        courseCode: "CSC309H1S"
      }, {
        courseCode: "CSC367H1S"
      }, {
        courseCode: "CSC258H1S"
      }, {
        courseCode: "CSC384H1S"
      }
    ]
    this.setState({ sections: sections });
  }

  getMeetings() {
    // TODO: dummy json
    const meetings = [
      {
        time: "2019-11-17T17:15:00.000Z",
        room: "BA1234",
        courseCode: "CSC302H1S"
      }, {
        time: "2019-11-18T17:15:00.000Z",
        room: "BA1234",
        courseCode: "CSC302H1S"
      }
    ]
    this.setState({ meetings: meetings })
  }

  render() {
    const { courses, sections, meetings } = this.state;
    const isProf = this.props.user && this.props.user.role === "PROFESSOR";

    const studentView = (
      <div id="dashboard">
        <div id="sections">
          <h2>Current Courses</h2>
          {sections.map(s => (
            <LectureSection section={s} key={s.courseCode} />
          ))}
        </div>
        <div id="meetings">
          <h2>Upcoming Meetings</h2>
          {meetings.map(m => (
            <Meeting meeting={m} key={m.courseCode + m.time} />
          ))}
        </div>
      </div>
    );

    const profView = (
      <div id="dashboard">
        <div id="courses">
          <h2>Current Courses</h2>
          {courses.map(c => (
            <Course course={c} key={c.name} />
          ))}
        </div>
        <div id="meetings">
          <h2>Upcoming Meetings</h2>
          {meetings.map(m => (
            <Meeting meeting={m} key={m.courseCode + m.time} />
          ))}
        </div>
      </div>
    );

    return isProf ? profView : studentView;
  }
}

export default Home;
