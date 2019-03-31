import React, { PureComponent } from 'react';
import { Link } from 'react-router-dom';

class LectureSectionCard extends PureComponent {
  render() {
    const { section, verbose } = this.props;
    return (
      <Link
        to={
          verbose
            ? {
                pathname: '/section',
                search: `?course=${section.course.courseCode}&year=${
                  section.year
                }&semester=${section.semester}&sectionCode=${
                  section.sectionCode
                }`
              }
            : {
                pathname: '/section',
                search: `?course=${section.course.courseCode}`
              }
        }
      >
        <div
          className={
            verbose
              ? 'card-element lecture-section-verbose'
              : 'card-element lecture-section'
          }
        >
          {verbose ? (
            <div>
              year: {section.year}
              <br />
              semester: {section.semester}
              <br />
              students: {section.numStudents}
            </div>
          ) : null}
        </div>
      </Link>
    );
  }
}

export default LectureSectionCard;
