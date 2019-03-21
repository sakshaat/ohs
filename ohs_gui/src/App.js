import React, { Component } from 'react';

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from "./components/Home";

import './App.css';

/* A wrapper which keeps track of the current logged in user, and provides the nav bar */
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
                <a href="/">
                  OHS
                </a>
              </div>
              {this.state.user &&
                <div className="nav-item">
                  Logged In a {this.state.user.role}
                </div>
              } 
            </div>
          </nav>
          {this.state.user &&
            <div className="App-body">
              <Switch>
                <Route path="/" render={() => <Home user={this.state.user} />} />
              </Switch>
            </div>
          }
        </div>
      </Router>
    );
  }
}

export default App;
