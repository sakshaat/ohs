import React, { Component } from 'react';

import { BrowserRouter as Router, Switch, Route, Redirect} from "react-router-dom";

import CreateCourse from "./components/CreateCourse"
import CreateSection from './components/CreateSection';

import './App.css';


class App extends Component {
  componentDidMount() {
    fetch('/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({"query": "query myQuery { courses { courseCode } }"}),
    }).then(res => console.log(res)) 
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
            <header className="App-header">
            <Switch>
                <Route exact path="/" render={() => <Redirect to='/add_course' />} />
                <Route exact path="/add_course" render={() => <CreateCourse />} />
                <Route exact path="/add_section" render={() => <CreateSection />} />
            </Switch>
            </header>
          </div>
        </Router>
    );
  }
}

export default App;
