import React, { PureComponent } from 'react';
import { toast } from 'react-toastify';
import { Query } from 'react-apollo';

import CreateOfficeHours from './CreateOfficeHours';
import BookMeetings from './BookMeetings';

import { GET_SECTION } from '../utils/queries';
import { userIsProf, getFormattedSectionName } from '../utils/helpers';

import './LectureSection.css';

class LectureSection extends PureComponent {
  render() {
    const { location, user } = this.props;

    const params = new URLSearchParams(location.search);
    const variables = {
      course: { courseCode: params.get('course') },
      year: params.get('year'),
      semester: params.get('semester'),
      sectionCode: params.get('sectionCode')
    };

    const isProf = userIsProf(user);

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
              <>
                <div className="section-info">
                  <h1>{getFormattedSectionName(section)}</h1>
                  <div>number of students: {section.numStudents}</div>
                </div>
                {isProf ? <CreateOfficeHours /> : <BookMeetings />}
              </>
            );
          }
          return null;
        }}
      </Query>
    );
  }
}

export default LectureSection;
