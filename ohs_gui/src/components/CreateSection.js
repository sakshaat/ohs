import React, { Component } from 'react';
import ReactDOM from 'react-dom'
import {Redirect} from "react-router-dom";

import ApolloClient from "apollo-boost";
import gql from "graphql-tag";

import shortid from 'shortid';
import { Button, FormGroup, FormControl} from 'react-bootstrap';

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

const GET_COURSES = gql`
    query getAllCourses {
        courses {
        courseCode
        }
    }`;

class CreateSection extends Component {
  constructor(props){
    super(props);
    this.state = {
        pickedCourse : null,
        sectionCreated: false,
        courseList: []
    }

    this.coursePicked = this.coursePicked.bind(this);
    this.createSection = this.createSection.bind(this);
    this.updateCourseList = this.updateCourseList.bind(this);
  }

  updateCourseList(res) {
    let courses = res.data.courses;
    let lst = courses.map(elem => elem.courseCode);
    this.setState({courseList: lst});
  }

  componentDidMount() {
    client
    .query({
        query: GET_COURSES
    })
    .then(res => this.updateCourseList(res))
    .catch(result => console.log(result));
  }

  coursePicked() {
    let course = ReactDOM.findDOMNode(this.refs.selectedCourse).value;

    // update course if its not the same one we have or null
    if(course && course !== this.state.pickedCourse) {
        this.setState({pickedCourse: course})
    }
    
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
                {courseCode: this.state.pickedCourse},
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
    .then(this.setState({sectionCreated: true}))
    .catch(res => console.log(res));
  }

  render() {
    if(this.state.sectionCreated) {
        return (<Redirect to="/"></Redirect>)
    }

    let courseItems = this.state.courseList
        .map(elem => <option key={shortid.generate()} value={elem}>{elem}</option>);

    let courseComponent = (
        <div>
            <h1>Pick a course</h1>
            <select ref="selectedCourse" onChange={this.coursePicked}>
                <option style={{display:"none"}}></option>
                {courseItems}
            </select>
        </div>
    )

    let sectionComponent = null;
    if(this.state.pickedCourse) {
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
            {courseComponent}
            {sectionComponent}
        </section>
      );
    }
  }


export default CreateSection;