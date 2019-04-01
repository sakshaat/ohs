import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Redirect } from 'react-router-dom';
import gql from 'graphql-tag';

import { Button, FormGroup, FormControl } from 'react-bootstrap';

import './CreateSection.css';
import { getProfClient } from '../utils/client';

const client = getProfClient();

const ADD_SECTION = gql`
  mutation addSection($sectionInput: SectionInput!) {
    createSection(sectionInput: $sectionInput) {
      sectionCode
    }
  }
`;
class CreateSection extends Component {
  constructor(props) {
    super(props);
    const {
      match: {
        params: { courseCode }
      }
    } = this.props;
    this.state = {
      sectionCreated: false,
      courseCode
    };

    this.createSection = this.createSection.bind(this);
  }

  createSection() {
    const { courseCode } = this.state;
    const {
      user: { id }
    } = this.props;

    const lsVal = ReactDOM.findDOMNode(this.refs.lsInput).value;
    const yearVal = ReactDOM.findDOMNode(this.refs.yearInput).value;
    const semesterVal = ReactDOM.findDOMNode(this.refs.semesterSelect).value;
    const snumVal = ReactDOM.findDOMNode(this.refs.studentInput).value;

    // variable
    const sectionInput = {
      course: { courseCode },
      year: yearVal,
      semester: semesterVal,
      sectionCode: lsVal,
      numStudents: snumVal,
      taughtBy: id
    };

    // send request
    client
      .mutate({
        mutation: ADD_SECTION,
        variables: {
          sectionInput
        }
      })
      .then(this.setState({ sectionCreated: true }))
      .catch(res => console.log(res));
  }

  render() {
    const { sectionCreated, courseCode, pickedCourse } = this.state;

    if (sectionCreated) {
      return <Redirect to={`/course/${courseCode}`} />;
    }

    const sectionComponent = (
      <div>
        <h1>Add a new Section to {pickedCourse}</h1>
        <FormGroup role="form">
          <FormControl
            ref="lsInput"
            placeholder="Section"
            aria-label="Section"
            aria-describedby="basic-addon2"
          />

          <FormControl
            ref="yearInput"
            placeholder="Year"
            aria-label="Year"
            aria-describedby="basic-addon2"
            type="number"
          />

          <FormControl
            ref="studentInput"
            placeholder="student"
            aria-label="student"
            aria-describedby="basic-addon2"
            type="number"
          />

          <select ref="semesterSelect" onChange={this.coursePicked}>
            <option value="WINTER">WINTER</option>
            <option value="FALL">FALL</option>
            <option value="SUMMER">SUMMER</option>
            <option value="FULL_YEAR">FULL_YEAR</option>
          </select>

          <br />

          <Button variant="secondary" onClick={this.createSection}>
            Create a Section
          </Button>
        </FormGroup>
      </div>
    );

    return <section className="container">{sectionComponent}</section>;
  }
}

export default CreateSection;
