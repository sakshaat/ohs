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

  getMeetings() {
    // TODO: dummy json
    const meetings = [
      {
        time: "2019-11-17T17:15:00.000Z",
        room: "BA1234",
        courseCode: "CSC302H1S",
        id: 11
      }, {
        time: "2019-11-18T17:15:00.000Z",
        room: "BA1234",
        courseCode: "CSC302H1S",
        id: 12
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
            <LectureSection section={s} key={s.id} />
          ))}
        </div>
        <div id="meetings">
          <h2>Upcoming Meetings</h2>
          {meetings.map(m => (
            <Meeting meeting={m} key={m.id} />
          ))}
        </div>
      </div>
    );

    const profView = (
      <div id="dashboard">
        <div id="courses">
          <h2>Current Courses</h2>
          {courses.map(c => (
            <Course course={c} key={c.id} />
          ))}
        </div>
        <div id="meetings">
          <h2>Upcoming Meetings</h2>
          {meetings.map(m => (
            <Meeting meeting={m} key={m.id} />
          ))}
        </div>
      </div>
    );

    return isProf ? profView : studentView;
  }
}

export default Home;
