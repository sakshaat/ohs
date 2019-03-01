import React, { Component } from 'react';
import ReactDOM from 'react-dom'
import './Course.css';
import {Redirect} from "react-router-dom";
import { Button, FormGroup, FormControl} from 'react-bootstrap';

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
    // send request here


    // if succeed
    this.setState({courseCreated: true});
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
