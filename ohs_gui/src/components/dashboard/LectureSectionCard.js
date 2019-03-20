import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class LectureSectionCard extends Component {
  render() {
    const section = this.props.section;
    return (
      <Link to={`/lectureSection/${this.props.section.id}`}>
        <div className={this.props.verbose ? "card-element lecture-section-verbose" : "card-element lecture-section"}>
          {this.props.verbose ?
            (
              <div>
                year: {section.year}
                <br />
                semester: {section.semester}
                <br />
                students: {section.numStudents}
              </div>
            )
            :
            section.courseCode
          }
        </div>
      </Link>
    );
  }
}

export default LectureSectionCard;
