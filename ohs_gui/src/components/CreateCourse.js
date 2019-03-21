import React, { Component } from 'react';
import ReactDOM from 'react-dom'

import {Redirect} from "react-router-dom";
import { Button, FormGroup, FormControl} from 'react-bootstrap';

import ApolloClient from "apollo-boost";
import gql from "graphql-tag";

import './CreateCourse.css';

const client = new ApolloClient({
  uri: "http://127.0.0.1:8000/graphql"
});

const ADD_COURSE = gql`
  mutation addCourse($courseInput: CourseInput!){
    createCourse(courseInput: $courseInput) {
      courseCode
    }
  }`;

class CreateCourse extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      courseCreated : false
     }
    
    this.createCourse = this.createCourse.bind(this);
  }

  createCourse() {
    let elem = ReactDOM.findDOMNode(this.refs.ccInput);
    let value = elem.value;
    
    // send request
    client
    .mutate({
      mutation: ADD_COURSE,
      variables: {
        courseInput: {"courseCode": value},
      },
    })
    .then(this.setState({courseCreated: true}))
    // send message back to dashboard
    .then(this.props.callback(value))
    .catch(res => console.log(res));
  }

  render() {
    if(this.state.courseCreated) {
      return (<Redirect to="/"></Redirect>);
    }
    return (
      <section className="container">
        <h1>Add a new Course</h1>
        <FormGroup role="form">
          <FormControl ref="ccInput"
            placeholder="CSCXYZ"
            aria-label="CSCXYZ"
            aria-describedby="basic-addon2"
            id="course-code-input"
          />
          <Button variant="secondary" onClick={this.createCourse}>Create a Course</Button>
        </FormGroup>
      </section>
    );
  }
}

export default CreateCourse;
