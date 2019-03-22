import React, { Component } from 'react';

import { BrowserRouter as Router} from "react-router-dom";
import Home from "./components/Home";
import Login from "./components/Login";

import './App.css';

/* A wrapper which keeps track of the current logged in user, and provides the nav bar */
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null,
      isLoggedIn: window.sessionStorage.token ? true : false
    }

    this.getUser = this.getUser.bind(this);
    this.notifyLogIn = this.notifyLogIn.bind(this);
    this.logout = this.logout.bind(this);
  }

  notifyLogIn(token) {
    window.sessionStorage.token = token;
    this.getUser();
    this.setState({isLoggedIn: true});
    
  }

  // TODO: we should set the user in state when we log in
  componentDidMount() {
    this.getUser();
    if(window.sessionStorage.token !== undefined) {
      this.getUser();
    }
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

  logout(e) {
    window.sessionStorage.removeItem("token");
    this.setState({isLoggedIn: false});
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
                this.state.user &&
                  [
                    <div key={0} className="nav-item">
                      Logged In as a {this.state.user.role}
                    </div>,
                    <div key={1} onClick={this.logout} className="logout-btn nav-item">
                      Logout
                    </div>
                  ]
                
              }
            </div>
          </nav>
          <div className="app-container">
            {this.state.isLoggedIn && this.state.user ? <Home user={this.state.user} /> : <Login notifyLogIn={(token)=>this.notifyLogIn(token)}/>}
          </div>

          
        </div>
      </Router>
    );
  }
}

export default App;
