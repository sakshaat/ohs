import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { toast } from 'react-toastify';
import { Redirect } from 'react-router-dom';
import { Button, FormGroup, FormControl } from 'react-bootstrap';
import gql from 'graphql-tag';
import { getProfClient } from '../utils/client';

import './CreateCourse.css';

const client = getProfClient();

const ADD_COURSE = gql`
  mutation addCourse($courseInput: CourseInput!) {
    createCourse(courseInput: $courseInput) {
      courseCode
    }
  }
`;
class CreateCourse extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courseCreated: false
    };

    this.createCourse = this.createCourse.bind(this);
  }

  createCourse() {
    const elem = ReactDOM.findDOMNode(this.refs.ccInput);
    const { value } = elem;
    const { callback } = this.props;

    // send request
    client
      .mutate({
        mutation: ADD_COURSE,
        variables: {
          courseInput: { courseCode: value }
        }
      })
      .then(() => {
        this.setState({ courseCreated: true });
        // send message back to dashboard
        callback(value);
      })
      .catch(() =>
        toast('Unknown Error - Could not create new course', {
          type: toast.TYPE.ERROR
        })
      );
  }

  render() {
    const { courseCreated } = this.state;

    if (courseCreated) {
      return <Redirect to="/" />;
    }
    return (
      <section className="container">
        <h1>Add a new Course</h1>
        <FormGroup role="form">
          <FormControl
            ref="ccInput"
            placeholder="CSCXYZ"
            aria-label="CSCXYZ"
            aria-describedby="basic-addon2"
            id="course-code-input"
          />
          <Button variant="secondary" onClick={this.createCourse}>
            Create a Course
          </Button>
        </FormGroup>
      </section>
    );
  }
}

export default CreateCourse;
