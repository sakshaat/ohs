import React, { Component } from 'react';
import MeetingCard from "./dashboard/MeetingCard"
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import CreateCourse from "./CreateCourse"
import CreateSection from './CreateSection';
import LectureSection from './LectureSection';
import Meeting from './Meeting';
import Course from './Course';
import Dashboard from './Dashboard';

import "./Home.css"

/* A wrapper which provides the meetings sidebar */
class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      meetings: []
    }

    this.getMeetings = this.getMeetings.bind(this);
  }

  componentDidMount() {
    this.getMeetings();
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
    const { meetings } = this.state;

    return (
      <Router>
        <div id="dashboard">
          <div id="meetings">
            <h2>Upcoming Meetings</h2>
            {meetings.map(m => (
              <MeetingCard meeting={m} key={m.id} />
            ))}
          </div>
          <div id="main">
            <Switch>
              <Route exact path="/" render={() => <Dashboard user={this.props.user} />} />
              <Route exact path="/meeting/:id" render={(props) => <Meeting user={this.props.user} {...props} />} />
              <Route exact path="/course/:course_code" render={(props) => <Course user={this.props.user} {...props} />} />
              <Route exact path="/lectureSection" render={(props) => <LectureSection user={this.props.user} {...props} />} />
              <Route exact path="/addCourse" render={() => <CreateCourse user={this.props.user} />} />
              <Route exact path="/course/:course_code/addSection" render={(props) => <CreateSection user={this.props.user} {...props} />} />
            </Switch>
          </div>
        </div>
      </Router>
    );
  }
}

export default Home;
