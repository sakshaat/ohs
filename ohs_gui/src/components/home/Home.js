import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { toast } from 'react-toastify';

import MeetingCard from '../dashboard/MeetingCard';

import CreateCourse from '../course/CreateCourse';
import CreateSection from '../lectureSection/CreateSection';
import LectureSection from '../lectureSection/LectureSection';
import Meeting from '../meeting/Meeting';
import Course from '../course/Course';
import { getProfClient } from '../utils/client';
import { roles } from '../utils/constants';

import { GET_COURSES, GET_SECTIONS } from '../utils/queries';

import './Home.css';
import ProfessorDashboard from '../dashboard/ProfessorDashboard';
import StudentDashboard from '../dashboard/StudentDashboard';

const client = getProfClient();

/* A wrapper which provides the meetings sidebar */
class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      meetings: [],
      courses: [],
      sections: []
    };

    this.updateMeetingsList = this.updateMeetingsList.bind(this);
    this.updateCourseList = this.updateCourseList.bind(this);
    this.updateSectionList = this.updateSectionList.bind(this);
    this.addCourse = this.addCourse.bind(this);
  }

  componentDidMount() {
    const { user } = this.props;
    const isProf = user.role === roles.PROFESSOR;

    if (isProf) {
      this.getCourses();
    } else {
      this.getSections();
    }
    this.updateMeetingsList();
  }

  getCourses() {
    // fetch courses
    client
      .query({
        query: GET_COURSES
      })
      .then(res => this.updateCourseList(res))
      .catch(() =>
        toast('Unknown Error - Cannot Retrieve Courses', {
          type: toast.TYPE.ERROR
        })
      );
  }

  getSections() {
    // fetch sections
    client
      .query({
        query: GET_SECTIONS
      })
      .then(res => this.updateSectionList(res))
      .catch(() =>
        toast('Unknown Error - Cannot Retrieve Sections', {
          type: toast.TYPE.ERROR
        })
      );
  }

  updateSectionList(res) {
    this.setState({ sections: res.data.sections });
  }

  addCourse(course) {
    const { courses } = this.state;
    this.setState({ courses: [...courses, course] });
  }

  updateCourseList(res) {
    const { courses } = res.data;
    const lst = courses.map(elem => elem.courseCode);
    this.setState({ courses: lst });
  }

  updateMeetingsList() {
    // TODO: dummy json
    const meetings = [
      {
        time: '2019-11-17T17:15:00.000Z',
        room: 'BA1234',
        courseCode: 'CSC302H1S',
        student: 'Pika Chu',
        professor: 'Alec Gibson',
        id: 11
      },
      {
        time: '2019-11-18T17:15:00.000Z',
        room: 'BA1234',
        courseCode: 'CSC302H1S',
        student: 'Pika Chu',
        professor: 'Alec Gibson',
        id: 12
      }
    ];
    this.setState({ meetings });
  }

  render() {
    const { meetings, courses, sections } = this.state;
    const { user } = this.props;
    const isProf = user && user.role === roles.PROFESSOR;

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
              <Route
                exact
                path="/"
                render={() =>
                  isProf ? (
                    <ProfessorDashboard courses={courses} />
                  ) : (
                    <StudentDashboard sections={sections} />
                  )
                }
              />
              <Route
                exact
                path="/meeting/:id"
                render={props => <Meeting user={user} {...props} />}
              />
              <Route
                exact
                path="/course/:courseCode"
                render={props => <Course user={user} {...props} />}
              />
              <Route
                exact
                path="/section"
                render={props => <LectureSection user={user} {...props} />}
              />
              <Route
                exact
                path="/add-course"
                render={() => (
                  <CreateCourse
                    user={user}
                    callback={course => this.addCourse(course)}
                  />
                )}
              />
              <Route
                exact
                path="/course/:course_code/add-section"
                render={props => <CreateSection user={user} {...props} />}
              />
            </Switch>
          </div>
        </div>
      </Router>
    );
  }
}

export default Home;
