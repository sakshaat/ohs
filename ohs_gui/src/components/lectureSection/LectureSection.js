import React, { PureComponent } from 'react';
import { toast } from 'react-toastify';
import { Query } from 'react-apollo';
import { Redirect } from 'react-router-dom';

import { Button } from 'react-bootstrap';

import { GET_SECTION } from '../utils/queries';

class LectureSection extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      redirectToAddStudents: false
    };
  }

  render() {
    const { location } = this.props;
    const { redirectToAddStudents } = this.state;
    const params = new URLSearchParams(location.search);

    const variables = {
      course: { courseCode: params.get('course') },
      year: params.get('year'),
      semester: params.get('semester'),
      sectionCode: params.get('sectionCode')
    };

    if (redirectToAddStudents) {
      return <Redirect to={`/add-students${location.search}`} />;
    }

    return (
      <div>
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
                  <Button
                    onClick={() =>
                      this.setState({ redirectToAddStudents: true })
                    }
                  >
                    Add Students
                  </Button>
                </div>
              );
            }
            return null;
          }}
        </Query>
      </div>
    );
  }
}

export default LectureSection;
