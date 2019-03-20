import React, { Component } from 'react';
import LectureSectionCard from "./dashboard/LectureSectionCard"
import { Link } from 'react-router-dom'

class Course extends Component {
  constructor(props) {
    super(props);
    this.state = {
      course: null,
      sections: []
    }

    this.getSections = this.getSections.bind(this);
    this.getCourse = this.getCourse.bind(this);
  }

  componentDidMount() {
    this.getCourse();
    this.getSections();
  }

  getSections() {
    // TODO: dummy json
    const sections = [
      {
        year: 2019,
        semester: "Winter",
        numStudents: 200,
        id: 6
      }, {
        year: 2019,
        semester: "Summer",
        numStudents: 200,
        id: 7
      }, {
        year: 2019,
        semester: "Fall",
        numStudents: 200,
        id: 8
      }
    ]
    this.setState({ sections: sections });
  }

  getCourse() {
    // TODO: dummy json
    const course = {
      name: "CSC302",
      id: this.props.match.params.id
    }
    this.setState({ course: course });
  }

  render() {
    const { course, sections } = this.state;
    return (
      <div id="sections">
        {course && <h2>{course.name} Lecture Sections</h2>}
        {sections.map(s => (
          <LectureSectionCard verbose section={s} key={s.id} />
        ))}
        {course && <Link to={`/course/${course.id}/addSection`}>
          <div className="add-section card-element">
            <span className="fa fa-plus"></span>
          </div>
        </Link>}
      </div>
    );
  }
}

export default Course;
