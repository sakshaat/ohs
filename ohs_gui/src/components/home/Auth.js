import React, { Component } from 'react';
import {
  Button,
  FormControl,
  ToggleButtonGroup,
  ToggleButton
} from 'react-bootstrap';
import ReactDOM from 'react-dom';

import './Auth.css';
import { PROF_BASE_URL } from '../utils/client';
import { PROFESSOR, STUDENT } from '../utils/constants';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedRole: null
    };
    this.register = this.register.bind(this);
    this.login = this.login.bind(this);
    this.userRegistered = this.userRegistered.bind(this);
    this.toggleRole = this.toggleRole.bind(this);
  }

  toggleRole(role) {
    this.setState({ selectedRole: role });
  }

  login() {
    const username = ReactDOM.findDOMNode(this.refs.loginUsernameInput).value;
    const password = ReactDOM.findDOMNode(this.refs.loginPwdInput).value;

    const url = `${PROF_BASE_URL}/get-token`;

    const data = {
      id: username,
      password
    };

    fetch(url, {
      method: 'POST', // or 'PUT'
      body: JSON.stringify(data), // data can be `string` or {object}!
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        }
        throw new Error(
          `'Network response was not ok - ${res.status}: ${res.statusText}`
        );
      })
      .then(response => this.userRegistered(response))
      .catch(error => console.error('Error:', error));
  }

  register() {
    const fname = ReactDOM.findDOMNode(this.refs.registerFnameInput).value;
    const lname = ReactDOM.findDOMNode(this.refs.registerLnameInput).value;
    const username = ReactDOM.findDOMNode(this.refs.registerUsernameInput)
      .value;
    const password = ReactDOM.findDOMNode(this.refs.registerPwdInput).value;

    const url = `${PROF_BASE_URL}/create-user`;

    const data = {
      id: username,
      password,
      firstName: fname,
      lastName: lname
    };

    fetch(url, {
      method: 'POST', // or 'PUT'
      body: JSON.stringify(data), // data can be `string` or {object}!
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        }
        throw new Error(
          `'Network response was not ok - ${res.status}: ${res.statusText}`
        );
      })
      .then(response => this.userRegistered(response))
      .catch(error => console.error('Error:', error));
  }

  userRegistered(res) {
    const { notifyLogIn } = this.props;
    notifyLogIn(res.token);
  }

  render() {
    const { selectedRole } = this.state;
    const authForm = (
      <section className="form-container">
        <section className="form login-form">
          <h1>Login</h1>
          <FormControl
            ref="loginUsernameInput"
            placeholder="Username"
            aria-label="username"
            aria-describedby="basic-addon2"
            id="login-username-input"
          />
          <FormControl
            ref="loginPwdInput"
            type="password"
            placeholder="Password"
            aria-label="Password"
            aria-describedby="basic-addon2"
            id="login-password-input"
          />
          <Button variant="secondary" onClick={this.login}>
            Login
          </Button>
        </section>
        <section className="form register-form">
          <h1>Register</h1>
          <FormControl
            ref="registerFnameInput"
            placeholder="First Name"
            aria-label="fname"
            aria-describedby="basic-addon2"
            id="register-fname-input"
          />
          <FormControl
            ref="registerLnameInput"
            placeholder="Last Name"
            aria-label="lname"
            aria-describedby="basic-addon2"
            id="register-lname-input"
          />
          <FormControl
            ref="registerUsernameInput"
            placeholder="Username"
            aria-label="username"
            aria-describedby="basic-addon2"
            id="register-username-input"
          />
          <FormControl
            ref="registerPwdInput"
            type="password"
            placeholder="Password"
            aria-label="Password"
            aria-describedby="basic-addon2"
            id="register-password-input"
          />
          <Button variant="secondary" onClick={this.register}>
            Register
          </Button>
        </section>
      </section>
    );
    return (
      <section className="auth-container">
        <h1>Professor Login/Registration</h1>

        <ToggleButtonGroup type="radio" name="roles" onChange={this.toggleRole}>
          <ToggleButton active size="lg" value={PROFESSOR}>
            Professor
          </ToggleButton>
          <ToggleButton size="lg" value={STUDENT}>
            Student
          </ToggleButton>
        </ToggleButtonGroup>

        {selectedRole ? authForm : null}
      </section>
    );
  }
}

export default Login;
