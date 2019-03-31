import React, { Component } from 'react';

import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { BrowserRouter as Router } from 'react-router-dom';

import Home from './components/home/Home';
import Auth from './components/home/Auth';

import './App.css';

// Have to call it once in your app.
toast.useLazyContainer();
toast.configure({
  autoClose: 2000,
  draggable: false,
  position: toast.POSITION.BOTTOM_RIGHT
});

/* A wrapper which keeps track of the current logged in user, and provides the nav bar */
class App extends Component {
  constructor(props) {
    super(props);
    const user = window.sessionStorage.user
      ? JSON.parse(window.sessionStorage.user)
      : null;
    this.state = {
      user,
      isLoggedIn: !!window.sessionStorage.token
    };

    this.notifyLogIn = this.notifyLogIn.bind(this);
    this.logout = this.logout.bind(this);
  }

  notifyLogIn(token, user) {
    window.sessionStorage.token = token;
    window.sessionStorage.user = JSON.stringify(user);
    this.setState({ user, isLoggedIn: true });
  }

  logout() {
    toast('Successfully Logged Out', { type: toast.TYPE.SUCCESS });
    window.sessionStorage.removeItem('token');
    window.sessionStorage.removeItem('user');
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
                    Logged In as {user.userName}
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
              <Auth
                notifyLogIn={(token, userObj) =>
                  this.notifyLogIn(token, userObj)
                }
              />
            )}
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
