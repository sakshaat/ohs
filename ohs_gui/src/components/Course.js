import React, { Component } from 'react';
import LectureSectionCard from "./dashboard/LectureSectionCard"
import { Link } from 'react-router-dom'
import shortid from 'shortid';

class Course extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sections: []
    }
  }

  componentDidMount() {
    this.getSections();
  }

  getSections() {
    // TODO: dummy json
    const sections = [
      {
        course: "CSC302",
        year: 2019,
        semester: "Winter",
        section_code: "H1S",
        num_students: 200
      }, {
        course: "CSC302",
        year: 2019,
        semester: "Summer",
        section_code: "H1S",
        num_students: 200
      }, {
        course: "CSC302",
        year: 2019,
        semester: "Fall",
        section_code: "H1S",
        num_students: 200
      }
    ]
    this.setState({ sections: sections });
  }

  render() {
    const { sections } = this.state;
    const course = this.props.match.params.course_code;
    return (
      <div id="sections">
        {course && <h1>{course} Lecture Sections</h1>}
        {sections.map(s => (
          <LectureSectionCard verbose section={s} key={shortid.generate()}/>
        ))}
        {course && this.props.user.role === "PROFESSOR" && <Link to={`/course/${course}/addSection`}>
          <div className="add-section card-element">
            <span className="fa fa-plus"></span>
          </div>
        </Link>}
      </div>
    );
  }
}

export default Course;
