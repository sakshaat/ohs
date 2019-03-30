import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class LectureSectionCard extends Component {
  render() {
    const section = this.props.section;
    return (
      <Link to={this.props.verbose ?
        { pathname: "/section", search: `?course=${section.course.courseCode}&year=${section.year}&semester=${section.semester}&section_code=${section.sectionCode}` }
        :
        { pathname: "/section", search: `?course=${section.course.courseCode}` }}>
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
            section.course
          }
        </div>
      </Link>
    );
  }
}

export default LectureSectionCard;
