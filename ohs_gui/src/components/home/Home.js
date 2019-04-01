import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { toast } from 'react-toastify';

import { ApolloProvider, Query } from 'react-apollo';
import { ApolloClient } from 'apollo-client';
import { createHttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { setContext } from 'apollo-link-context';

import MeetingCard from '../dashboard/MeetingCard';

import CreateCourse from '../course/CreateCourse';
import CreateSection from '../lectureSection/CreateSection';
import LectureSection from '../lectureSection/LectureSection';
import Meeting from '../meeting/Meeting';
import Course from '../course/Course';

import { roles } from '../utils/constants';

import { GET_COURSES, GET_SECTIONS } from '../utils/queries';

import './Home.css';
import ProfessorDashboard from '../dashboard/ProfessorDashboard';
import StudentDashboard from '../dashboard/StudentDashboard';

const PROF_BASE_URL = `${process.env.REACT_APP_INSTRUCTOR_SERVICE_URL ||
  'http://localhost:8000'}`;

const STUDENT_BASE_URL = `${process.env.REACT_APP_STUDENT_SERVICE_URL ||
  'http://localhost:8001'}`;

/* A wrapper which provides the meetings sidebar */
class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      meetings: []
    };
    this.updateMeetingsList = this.updateMeetingsList.bind(this);
  }

  componentDidMount() {
    this.updateMeetingsList();
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
    const { meetings } = this.state;
    const { user } = this.props;
    const isProf = user && user.role === roles.PROFESSOR;

    const httpLink = createHttpLink({
      uri: isProf ? `${PROF_BASE_URL}/graphql` : `${STUDENT_BASE_URL}/graphql`
    });

    const authLink = setContext((_, { headers }) => {
      // get the authentication token from local storage if it exists
      const token = window.sessionStorage.getItem('token');
      // return the headers to the context so httpLink can read them
      return {
        headers: {
          ...headers,
          Authorization: token ? `Bearer ${token}` : ''
        }
      };
    });

    const client = new ApolloClient({
      link: authLink.concat(httpLink),
      cache: new InMemoryCache()
    });

    return (
      <ApolloProvider client={client}>
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
                  render={() => {
                    return isProf ? (
                      <Query
                        query={GET_COURSES}
                        onError={() => {
                          toast('Unknown Error - Could not create new course', {
                            type: toast.TYPE.ERROR
                          });
                        }}
                      >
                        {({ data }) => {
                          const { courses } = data;
                          console.log(courses);
                          if (courses) {
                            const lst = courses.map(elem => elem.courseCode);
                            return <ProfessorDashboard courses={lst} />;
                          }

                          return null;
                        }}
                      </Query>
                    ) : (
                      <Query
                        query={GET_SECTIONS}
                        onError={() => {
                          toast('Unknown Error - Could not create new course', {
                            type: toast.TYPE.ERROR
                          });
                        }}
                      >
                        {({ data }) =>
                          data.sections && (
                            <StudentDashboard sections={data.sections} />
                          )
                        }
                      </Query>
                    );
                  }}
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
                      callback={() => this.courseAdded()}
                    />
                  )}
                />
                <Route
                  exact
                  path="/course/:courseCode/add-section"
                  render={props => <CreateSection user={user} {...props} />}
                />
              </Switch>
            </div>
          </div>
        </Router>
      </ApolloProvider>
    );
  }
}

export default Home;
