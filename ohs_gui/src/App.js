import React, { Component } from 'react';

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import CreateCourse from "./components/CreateCourse"
import CreateSection from './components/CreateSection';
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
      role: "STUDENT"
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

                {/* TODO: remove */}
                <Route exact path="/add_course" render={() => <CreateCourse />} />
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
