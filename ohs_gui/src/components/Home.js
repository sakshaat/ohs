import React, { Component } from 'react';
import MeetingCard from "./dashboard/MeetingCard"
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import CreateCourse from "./CreateCourse"
import CreateSection from './CreateSection';
import LectureSection from './LectureSection';
import Meeting from './Meeting';
import Course from './Course';
import Dashboard from './Dashboard';

import { client } from "../utils/client";
import { GET_COURSES, GET_SECTIONS } from "../utils/queries"

import "./Home.css"

/* A wrapper which provides the meetings sidebar */
class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      meetings: [],
      courses: [],
      sections: []
    }

    this.updateMeetingsList = this.updateMeetingsList.bind(this);
    this.updateCourseList = this.updateCourseList.bind(this);
    this.updateSectionList = this.updateSectionList.bind(this);
    this.addCourse = this.addCourse.bind(this);
  }

  componentDidMount() {
    this.updateMeetingsList();
    const isProf = this.props.user && this.props.user.role === "PROFESSOR";

    if(isProf) {
      this.getCourses()
    } else {
      this.getSections();
    }
    
  }

  getCourses() {
    // fetch courses
    client
      .query({
          query: GET_COURSES
      })
      .then(res => this.updateCourseList(res))
      .catch(result => console.log(result));
  }

  addCourse(course) {
    this.setState({courses: [...this.state.courses, course]});
  }

  updateCourseList(res) {
    let courses = res.data.courses;
    let lst = courses.map(elem => elem.courseCode);
    this.setState({courses: lst});
  }

  updateSectionList(res) {
    this.setState({sections: res.data.sections});
  }

  getSections() {
    // fetch sections
    client
      .query({
          query: GET_SECTIONS
      })
      .then(res => this.updateSectionList(res))
      .catch(result => console.log(result));

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

  updateMeetingsList() {
    // TODO: dummy json
    const meetings = [
      {
        time: "2019-11-17T17:15:00.000Z",
        room: "BA1234",
        courseCode: "CSC302H1S",
        student: "Pika Chu",
        professor: "Alec Gibson",
        id: 11
      }, {
        time: "2019-11-18T17:15:00.000Z",
        room: "BA1234",
        courseCode: "CSC302H1S",
        student: "Pika Chu",
        professor: "Alec Gibson",
        id: 12
      }
    ]
    this.setState({ meetings: meetings })
  }

  render() {
    const { meetings } = this.state;
    const isProf = this.props.user && this.props.user.role === "PROFESSOR";

    return (
      <Router>
        <div id="dashboard">
          <div id="meetings">
            <h2>Upcoming Meetings</h2>
            {meetings.map(m => (
                <MeetingCard isProf={isProf} meeting={m} key={m.id} />
            ))}
          </div>
          <div id="main">
            <Switch>
              <Route exact path="/" render={() => <Dashboard user={this.props.user} courses={this.state.courses} sections={this.state.sections} />} />
              <Route exact path="/meeting/:id" render={(props) => <Meeting user={this.props.user} {...props} />} />
              <Route exact path="/course/:course_code" render={(props) => <Course user={this.props.user} {...props} />} />
              <Route exact path="/section" render={(props) => <LectureSection user={this.props.user} {...props} />} />
              <Route exact path="/add-course" render={() => <CreateCourse user={this.props.user} callback={(course) => this.addCourse(course)}/>} />
              <Route exact path="/course/:course_code/add-section" render={(props) => <CreateSection user={this.props.user} {...props} />} />
            </Switch>
          </div>
        </div>
      </Router>
    );
  }
}

export default Home;
