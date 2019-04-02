import React, { PureComponent } from 'react';
import { toast } from 'react-toastify';
import { Query } from 'react-apollo';

import { GET_SECTION } from '../utils/queries';

class LectureSection extends PureComponent {
  render() {
    const { location } = this.props;
    const params = new URLSearchParams(location.search);

    const variables = {
      course: { courseCode: params.get('course') },
      year: params.get('year'),
      semester: params.get('semester'),
      sectionCode: params.get('sectionCode')
    };

    return (
      <Query
        query={GET_SECTION}
        variables={variables}
        onError={() => {
          toast('Unknown Error - Could not find the section', {
            type: toast.TYPE.ERROR
          });
        }}
      >
        {({ data }) => {
          const { section } = data;
          if (section) {
            return (
              <div>
                LectureSection for {section.course.courseCode}
                <div>
                  year: {section.year}
                  <br />
                  semester: {section.semester}
                  <br />
                  section_code: {section.sectionCode}
                  <br /># of students: {section.numStudents}
                </div>
              </div>
            );
          }
          return null;
        }}
      </Query>
    );
  }
}

export default LectureSection;
