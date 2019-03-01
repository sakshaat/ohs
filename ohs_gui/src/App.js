import React, { Component } from 'react';
import Course from "./components/Course"
import { BrowserRouter as Router, Switch, Route, Redirect} from "react-router-dom";

import './App.css';
import Section from './components/Section';
import Dashboard from './components/Dashboard';

class App extends Component {
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
          <header className="App-header">
          <Switch>
              <Route exact path="/" render={() => <Redirect to='/add_course' />} />
              <Route exact path="/add_course" render={() => <Course />} />
              <Route exact path="/add_section" render={() => <Section />} />
              <Route exact path="/dashboard" render={() => <Dashboard />} />
          </Switch>
          </header>
        </div>
      </Router>
    );
  }
}

export default App;
