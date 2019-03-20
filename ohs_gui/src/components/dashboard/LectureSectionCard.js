import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class LectureSectionCard extends Component {
  render() {
    const section = this.props.section;
    return (
      <Link to={this.props.verbose ?
        { pathname: "/lectureSection", search: `?course=${section.course}&year=${section.year}&semester=${section.semester}&section_code=${section.section_code}` }
        :
        { pathname: "/lectureSection", search: `?course=${section.course}` }}>
        <div className={this.props.verbose ? "card-element lecture-section-verbose" : "card-element lecture-section"}>
          {this.props.verbose ?
            (
              <div>
                year: {section.year}
                <br />
                semester: {section.semester}
                <br />
                students: {section.num_students}
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
