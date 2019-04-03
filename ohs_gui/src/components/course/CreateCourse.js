import React, { Component } from 'react';
import { toast } from 'react-toastify';
import { Redirect } from 'react-router-dom';
import { Button, FormGroup, FormControl } from 'react-bootstrap';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';

import './CreateCourse.css';

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
      courseCreated: false,
      courseText: ''
    };
  }

  render() {
    const { courseCreated, courseText } = this.state;
    const { callback } = this.props;
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
            onChange={e => this.setState({ courseText: e.target.value })}
          />
          {courseText && (
            <Mutation
              mutation={ADD_COURSE}
              variables={{ courseInput: { courseCode: courseText } }}
              options={{
                refetchQueries: ['getCourses']
              }}
              onCompleted={() => {
                this.setState({ courseCreated: true });
                callback();
                toast('New Course Created', {
                  type: toast.TYPE.SUCCESS
                });
              }}
              onError={() => {
                toast('Unknown Error - Could not create new course', {
                  type: toast.TYPE.ERROR
                });
              }}
            >
              {(mut, { loading }) => {
                return (
                  <div>
                    {loading && <p>Loading...</p>}
                    <Button variant="secondary" onClick={mut}>
                      Create a Course
                    </Button>
                  </div>
                );
              }}
            </Mutation>
          )}
        </FormGroup>
      </section>
    );
  }
}

export default CreateCourse;
