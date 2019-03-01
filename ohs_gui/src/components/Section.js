import React, { Component } from 'react';
import './Section.css';
import ReactDOM from 'react-dom'
import { Button, FormGroup, FormControl} from 'react-bootstrap';
import {Redirect} from "react-router-dom";

class Section extends Component {
  constructor(props){
    super(props);
    this.state = {
        pickedCourse : null,
        sectionCreated: false
    }

    this.coursePicked = this.coursePicked.bind(this);
    this.createSection = this.createSection.bind(this);
  }

  coursePicked() {
      let course = ReactDOM.findDOMNode(this.refs.selectedCourse).value;
      this.setState({pickedCourse: course})
  }

  createSection() {
    let elem = ReactDOM.findDOMNode(this.refs.lsInput);
    let value = elem.value;
    // send request here


    // if succeed
    this.setState({sectionCreated: true});
  }


  render() {

    if(this.state.sectionCreated) {
        return (<Redirect to="/dashboard"></Redirect>)
    }

    let courseComponent = (
        <div>
            <h1>Pick a course</h1>
            <select ref="selectedCourse" onChange={this.coursePicked}>
                <option disabled selected value> -- select a course -- </option>
                <option value="CSCXYZ">CSCXYZ</option>
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
                    placeholder="LEC001"
                    aria-label="LEC001"
                    aria-describedby="basic-addon2"
                    id="course-code-input"
                />
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


export default Section;