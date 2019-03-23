import React, { Component } from 'react';

import { BrowserRouter as Router } from 'react-router-dom';
import Home from './components/home/Home';
import Auth from './components/home/Auth';

import './App.css';

/* A wrapper which keeps track of the current logged in user, and provides the nav bar */
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null,
      isLoggedIn: !!window.sessionStorage.token
    };

    this.getUser = this.getUser.bind(this);
    this.notifyLogIn = this.notifyLogIn.bind(this);
    this.logout = this.logout.bind(this);
  }

  // TODO: we should set the user in state when we log in
  componentDidMount() {
    this.getUser();
    if (window.sessionStorage.token !== undefined) {
      this.getUser();
    }
  }

  getUser() {
    // TODO: dummy json
    const user = {
      role: 'PROFESSOR',
      firstName: 'Alec',
      lastName: 'Gibson',
      id: 'a'
    };
    this.setState({ user });
  }

  notifyLogIn(token) {
    window.sessionStorage.token = token;
    this.getUser();
    this.setState({ isLoggedIn: true });
  }

  logout() {
    window.sessionStorage.removeItem('token');
    this.setState({ isLoggedIn: false });
  }

  render() {
    const { isLoggedIn, user } = this.state;
    return (
      <Router>
        <div className="App">
          <nav>
            <div className="links">
              <div className="nav-item">
                <a tabIndex={0} href="/">
                  OHS
                </a>
              </div>
              {isLoggedIn &&
                user && [
                  <div key={0} className="nav-item">
                    Logged In as {user.role} {user.id}
                  </div>,
                  <div
                    key={1}
                    onClick={this.logout}
                    role="button"
                    tabIndex={-1}
                    onKeyPress={this.logout}
                    className="logout-btn nav-item"
                  >
                    Logout
                  </div>
                ]}
            </div>
          </nav>
          <div className="app-container">
            {isLoggedIn && user ? (
              <Home user={user} />
            ) : (
              <Auth notifyLogIn={token => this.notifyLogIn(token)} />
            )}
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
