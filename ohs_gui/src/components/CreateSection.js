import React, { Component } from 'react';
import ReactDOM from 'react-dom'
import { Redirect } from "react-router-dom";

import ApolloClient from "apollo-boost";
import gql from "graphql-tag";

import { Button, FormGroup, FormControl } from 'react-bootstrap';

import './CreateSection.css';

const client = new ApolloClient({
  uri: "http://127.0.0.1:8000/graphql"
});

const ADD_SECTION = gql`
    mutation addSection($sectionInput: SectionInput!) {
        createSection(sectionInput: $sectionInput) {
            sectionCode
        }
    }`;

class CreateSection extends Component {
  constructor(props) {
    super(props);
    this.state = {
      pickedCourse: null,
      sectionCreated: false
    }

    this.createSection = this.createSection.bind(this);
  }

  componentDidMount() {
    // TODO: use this.props.match.params.id to fetch course name.
    const pickedCourse = "CSC302"
    this.setState({ pickedCourse: pickedCourse })
  }

  createSection() {
    let lsVal = ReactDOM.findDOMNode(this.refs.lsInput).value;
    let yearVal = ReactDOM.findDOMNode(this.refs.yearInput).value;
    let semesterVal = ReactDOM.findDOMNode(this.refs.semesterSelect).value;
    let snumVal = ReactDOM.findDOMNode(this.refs.studentInput).value;

    // variable
    let sectionInput =
    {
      course:
        { courseCode: this.state.pickedCourse },
      year: yearVal,
      semester: semesterVal,
      sectionCode: lsVal,
      numStudents: snumVal
    }

    // send request
    client
      .mutate({
        mutation: ADD_SECTION,
        variables: {
          sectionInput: sectionInput,
        },
      })
      .then(this.setState({ sectionCreated: true }))
      .catch(res => console.log(res));
  }

  render() {
    if (this.state.sectionCreated) {
      return (<Redirect to={"/course/" + this.props.match.params.id}></Redirect>)
    }

    let sectionComponent = null;
    if (this.state.pickedCourse) {
      sectionComponent = (
        <div>
          <h1>Add a new Section to {this.state.pickedCourse}</h1>
          <FormGroup role="form">

            <FormControl ref="lsInput"
              placeholder="Section"
              aria-label="Section"
              aria-describedby="basic-addon2"
            />

            <FormControl ref="yearInput"
              placeholder="Year"
              aria-label="Year"
              aria-describedby="basic-addon2"
              type="number"
            />

            <FormControl ref="studentInput"
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

            <Button variant="secondary" onClick={this.createSection}>Create a Section</Button>
          </FormGroup>
        </div>
      )
    }

    return (
      <section className="container">
        {sectionComponent}
      </section>
    );
  }
}

export default CreateSection;
