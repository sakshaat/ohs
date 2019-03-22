import React, { Component } from 'react';
import LectureSectionCard from "./dashboard/LectureSectionCard"
import { Link } from 'react-router-dom'
import shortid from 'shortid';
import {getClient} from "../utils/client"
import {GET_SECTION_FOR_COURSE} from "../utils/queries"
import "./Course.css";

const client = getClient();

class Course extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sections: []
    }

    this.updateSectionList = this.updateSectionList.bind(this);
    this.getSections = this.getSections.bind(this);
  }

  componentDidMount() {
    this.getSections();
  }

  updateSectionList(lst) {
    console.log(lst);
    this.setState({sections: lst});
  }

  getSections() {
    // query sectons for the particular course
    client
      .query({
          query: GET_SECTION_FOR_COURSE,
          variables: {
            sectionFilter: JSON.stringify({
              course: this.props.match.params.course_code,
              taughtBy: this.props.user.id
            })
          }
      })
      .then(res => this.updateSectionList(res.data.sections))
      .catch(result => console.log(result));
  }

  render() {
    const { sections } = this.state;
    const course = this.props.match.params.course_code;
    return (
      <div id="sections">
        <div className="container">
          <div className="row">
            <div className="header-cont col-10">
              {course && <h1>{course} Lecture Sections </h1>}
            </div>
            <div className="header-cont col-2">
            <i onClick={() => window.location.reload()} className="fa fa-refresh fa-3x" aria-hidden="true"></i>
            </div>
          </div>
        </div>
 
    
        {sections.map(s => (
          <LectureSectionCard verbose section={s} key={shortid.generate()}/>
        ))}
        {course && this.props.user.role === "PROFESSOR" && <Link to={`/course/${course}/add-section`}>
          <div className="add-section card-element">
            <span className="fa fa-plus"></span>
          </div>
        </Link>}
      </div>
    );
  }
}

export default Course;
