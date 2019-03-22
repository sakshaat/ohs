import React, { Component } from 'react';

import {getClient} from "../utils/client"
import {GET_SECTION} from "../utils/queries"

const client = getClient();

class LectureSection extends Component {
  constructor(props) {
    super(props);
    this.state = {
      section : {}
    }

    this.updateSection = this.updateSection.bind(this);
  }

  updateSection(section) {
    this.setState({section: section});
  }
  
  componentDidMount() {
    let params = new URLSearchParams(this.props.location.search);
    client
    .query({
        query: GET_SECTION,
        variables: {
          course: {courseCode: params.get("course")},
          year: params.get("year"),
          semester: params.get("semester"),
          sectionCode: params.get("section_code")
        }
    })
    .then(res => this.setState({section: res.data.section}))
    .catch(result => console.log(result));
  }

  render() {
    const section = this.state.section;

    return (
      Object.keys(section).length !== 0 ?     
        <div>
          LectureSection for {section.course.courseCode}
            <div>
              year: {section.year}
              <br />
              semester: {section.semester}
              <br />
              section_code: {section.sectionCode}
              <br />
              # of students: {section.numStudents}
            </div>
        </div> 
      : 
        null
      );
  }
}

export default LectureSection;
