import React, { Component } from 'react';

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from "./components/Home";
import Login from "./components/Login"

import './App.css';

/* A wrapper which keeps track of the current logged in user, and provides the nav bar */
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null,
      isLoggedIn: false
    }

    this.getUser = this.getUser.bind(this);
  }

  // TODO: we should set the user in state when we log in
  componentDidMount() {
    if(window.sessionStorage.token) {
      this.setState({isLoggedIn: true});
    }
    // this.getUser();
  }

  getUser() {
    // TODO: dummy json
    const user = {
      role: "PROFESSOR",
      first_name: "Alec",
      last_name: "Gibson"
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
              {this.state.isLoggedIn &&
                <div className="nav-item">
                  Logged In as a {this.state.user.role}
                </div>
              } 
            </div>
          </nav>
          <div className="app-container">
            {this.state.isLoggedIn ? <Home user={this.state.user} /> : <Login />}
          </div>

          
        </div>
      </Router>
    );
  }
}

export default App;
