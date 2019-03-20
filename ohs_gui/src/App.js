import React, { Component } from 'react';

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import CreateCourse from "./components/CreateCourse"
import CreateSection from './components/CreateSection';
import LectureSection from './components/LectureSection';
import Meeting from './components/Meeting';
import Course from './components/Course';

import Home from "./components/Home";

import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null
    }

    this.getUser = this.getUser.bind(this);
  }

  // TODO: we should set the user in state when we log in

  componentDidMount() {
    this.getUser();
  }

  getUser() {
    // TODO: dummy json
    const user = {
      role: "PROFESSOR"
    }
    this.setState({ user: user });
  }

  render() {
    return (
      <Router>
        <div className="App">
          <nav>
            <div className="links">
              <div className="nav-item">
                OHS
              </div>
              <div className="nav-item">
                Logged In as Dr. Frankenstein
              </div>
            </div>
          </nav>
          {this.state.user &&
            <div className="App-body">
              <Switch>
                <Route exact path="/" render={() => <Home user={this.state.user} />} />
                <Route exact path="/meeting/:id" render={(props) => <Meeting user={this.state.user} {...props} />} />
                <Route exact path="/course/:id" render={(props) => <Course user={this.state.user} {...props} />} />
                <Route exact path="/lectureSection/:id" render={(props) => <LectureSection user={this.state.user} {...props} />} />
                <Route exact path="/addCourse" render={() => <CreateCourse />} />

                {/* TODO: remove */}
                <Route exact path="/add_section" render={() => <CreateSection />} />
              </Switch>
            </div>
          }
        </div>
      </Router>
    );
  }
}

export default App;
