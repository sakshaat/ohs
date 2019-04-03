import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from 'react-router-dom';
import { toast } from 'react-toastify';

import { ApolloProvider, Query } from 'react-apollo';
import { ApolloClient } from 'apollo-client';
import { createHttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { setContext } from 'apollo-link-context';
import { onError } from 'apollo-link-error';
import { ApolloLink } from 'apollo-link';

import MeetingCard from '../dashboard/MeetingCard';

import CreateCourse from '../course/CreateCourse';
import CreateSection from '../lectureSection/CreateSection';
import LectureSection from '../lectureSection/LectureSection';
import Meeting from '../meeting/Meeting';
import Course from '../course/Course';
import AddStudentsToSection from '../lectureSection/AddStudentsToSection';

import { userIsProf } from '../utils/helpers';

import {
  GET_COURSES,
  GET_UPCOMING_MEETINGS,
  GET_SECTIONS_FOR_STUDENT
} from '../utils/queries';

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
      isAuth: true
    };
  }

  notAuth() {
    const { notifyUnauth } = this.props;
    notifyUnauth();
    this.setState({ isAuth: false });
  }

  render() {
    const { isAuth } = this.state;
    const { user } = this.props;
    const isProf = userIsProf(user);

    const httpLink = createHttpLink({
      uri: isProf ? `${PROF_BASE_URL}/graphql` : `${STUDENT_BASE_URL}/graphql`
    });

    const logoutLink = onError(({ networkError }) => {
      if (networkError.statusCode === 401) this.notAuth();
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

    const link = ApolloLink.from([logoutLink, authLink, httpLink]);

    const client = new ApolloClient({
      link,
      cache: new InMemoryCache()
    });

    return isAuth ? (
      <ApolloProvider client={client}>
        <Router>
          <div id="dashboard">
            <div id="meetings">
              <h2>Upcoming Meetings</h2>
              <Query
                query={GET_UPCOMING_MEETINGS}
                onError={() => {
                  toast('Unknown Error - Could not get upcoming meetings ', {
                    type: toast.TYPE.ERROR
                  });
                }}
              >
                {({ data }) => {
                  const { upcomingMeetings } = data;
                  if (upcomingMeetings && upcomingMeetings.length) {
                    const lst = upcomingMeetings.map(m => (
                      <MeetingCard isProf={isProf} meeting={m} key={m.id} />
                    ));
                    return lst;
                  }

                  return <div>No Upcoming Meetings</div>;
                }}
              </Query>
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
                          toast('Unknown Error - Could not get courses', {
                            type: toast.TYPE.ERROR
                          });
                        }}
                      >
                        {({ data }) => {
                          const { courses } = data;
                          if (courses) {
                            const lst = courses.map(elem => elem.courseCode);
                            return <ProfessorDashboard courses={lst} />;
                          }

                          return null;
                        }}
                      </Query>
                    ) : (
                      <Query
                        query={GET_SECTIONS_FOR_STUDENT}
                        variables={{ studentNum: user.studentNumber }}
                        onError={() => {
                          toast('Unknown Error - Could not get sections', {
                            type: toast.TYPE.ERROR
                          });
                        }}
                      >
                        {({ data }) => {
                          if (data.sections) {
                            return (
                              data.sections && (
                                <StudentDashboard sections={data.sections} />
                              )
                            );
                          }

                          return null;
                        }}
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
                  path="/add-students"
                  render={props => (
                    <AddStudentsToSection user={user} {...props} />
                  )}
                />
                <Route
                  exact
                  path="/add-course"
                  render={() => (
                    <CreateCourse
                      user={user}
                      callback={() => this.forceUpdate()}
                    />
                  )}
                />
                <Route
                  exact
                  path="/course/:courseCode/add-section"
                  render={props => (
                    <CreateSection
                      user={user}
                      callback={() => this.forceUpdate()}
                      {...props}
                    />
                  )}
                />
              </Switch>
            </div>
          </div>
        </Router>
      </ApolloProvider>
    ) : (
      <Redirect to="/" />
    );
  }
}

export default Home;
