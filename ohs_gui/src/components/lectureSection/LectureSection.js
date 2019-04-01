import React, { Component } from 'react';
import { toast } from 'react-toastify';

import { getProfClient } from '../utils/client';
import { GET_SECTION } from '../utils/queries';

const client = getProfClient();

class LectureSection extends Component {
  constructor(props) {
    super(props);
    this.state = {
      section: {}
    };

    this.updateSection = this.updateSection.bind(this);
  }

  componentDidMount() {
    const { location } = this.props;
    const params = new URLSearchParams(location.search);
    client
      .query({
        query: GET_SECTION,
        variables: {
          course: { courseCode: params.get('course') },
          year: params.get('year'),
          semester: params.get('semester'),
          sectionCode: params.get('sectionCode')
        }
      })
      .then(res => this.setState({ section: res.data.section }))
      .catch(() =>
        toast('Unknown Error - Could not get lecture session', {
          type: toast.TYPE.ERROR
        })
      );
  }

  updateSection(section) {
    this.setState({ section });
  }

  render() {
    const { section } = this.state;

    return Object.keys(section).length !== 0 ? (
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
    ) : null;
  }
}

export default LectureSection;
