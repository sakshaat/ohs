import React, { Component } from 'react';
import { Button, FormControl} from "react-bootstrap";
import ReactDOM from 'react-dom'

import './Login.css';

const URL = `${process.env.REACT_APP_INSTRUCTOR_SERVICE_URL || 'http://localhost:8000'}/create-user`

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {  }

        this.register = this.register.bind(this);
    }

    register() {
        let fname = ReactDOM.findDOMNode(this.refs.registerFnameInput).value;
        let lname = ReactDOM.findDOMNode(this.refs.registerLnameInput).value;
        let username = ReactDOM.findDOMNode(this.refs.registerUsernameInput).value;
        let password = ReactDOM.findDOMNode(this.refs.registerPwdInput).value;

        let data = {
            "id": username, 
            "password": password, 
            "firstName": fname, 
            "lastName": lname
        }

        fetch(URL, {
            method: 'POST', // or 'PUT'
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers:{
                'Content-Type': 'application/json'
            }}).then(res => res.json())
        .then(response => console.log('Success:', JSON.stringify(response)))
        .catch(error => console.error('Error:', error));
    }

    render() { 
        return ( 
            <section className="auth-container">
                <h1>Professor Login/Registration</h1>
                <section className="form-container">
                    <section className="form login-form">
                        <h1>Login</h1>
                        <FormControl ref="login-usernameInput"
                                placeholder="Username"
                                aria-label="username"
                                aria-describedby="basic-addon2"
                                id="login-username-input"
                            />
                        <FormControl ref="login-pwdInput"
                                type="password"
                                placeholder="Password"
                                aria-label="Password"
                                aria-describedby="basic-addon2"
                                id="login-password-input"
                            />
                        <Button variant="secondary" onClick={this.createCourse}>Login</Button>
                    </section>
                    <section className="form register-form">
                        <h1>Register</h1>
                        <FormControl ref="registerFnameInput"
                                placeholder="First Name"
                                aria-label="fname"
                                aria-describedby="basic-addon2"
                                id="register-fname-input"
                            />
                        <FormControl ref="registerLnameInput"
                                placeholder="Last Name"
                                aria-label="lname"
                                aria-describedby="basic-addon2"
                                id="register-lname-input"
                            />
                        <FormControl ref="registerUsernameInput"
                                placeholder="Username"
                                aria-label="username"
                                aria-describedby="basic-addon2"
                                id="register-username-input"
                            />
                        <FormControl ref="registerPwdInput"
                                type="password"
                                placeholder="Password"
                                aria-label="Password"
                                aria-describedby="basic-addon2"
                                id="register-password-input"
                            />
                        <Button variant="secondary" onClick={this.register}>Register</Button>
                    </section>
                </section> 
            </section>
        )
    }
}
 
export default Login;