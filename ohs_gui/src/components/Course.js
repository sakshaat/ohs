import React, { Component } from 'react';
import ReactDOM from 'react-dom'
import './Course.css';
import {Redirect} from "react-router-dom";
import { Button, FormGroup, FormControl} from 'react-bootstrap';

import ApolloClient from "apollo-boost";
import gql from "graphql-tag";

const client = new ApolloClient({
  uri: "http://127.0.0.1:8000/graphql"
});

const ADD_COURSE = gql`
  mutation addCourse($courseInput: CourseInput!){
    createCourse(courseInput: $courseInput) {
      courseCode
    }
  }`;

class Course extends Component {
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
    .catch(console.log("FAILED"));
  }

  render() {
    if(this.state.courseCreated) {
      return (<Redirect to="/add_section"></Redirect>);
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

export default Course;
