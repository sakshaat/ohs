import React, { Component } from 'react';
import OfficeHours from "./components/OfficeHour"
import Course from "./components/Course"
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";

import './App.css';

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <div className="nav">
            <div className="links">
              <Link to="/course">
                COURSES
            </Link>
              <Link to="/">
                HOME
            </Link>
            </div>
          </div>
          <header className="App-header">
            <Switch>
              <Route exact path="/" render={() => <OfficeHours slotNum={5}> </OfficeHours>} />
              <Route exact path="/course" render={() => <Course />} />
            </Switch>
          </header>
        </div>
      </Router>
    );
  }
}

export default App;
