import React, { PureComponent } from 'react';
import { toast } from 'react-toastify';
import { Query } from 'react-apollo';

import { GET_SECTION } from '../utils/queries';

import OHContainer from '../officeHours/OHContainer';
import './LectureSection.css';

class LectureSection extends PureComponent {
  render() {
    const { location } = this.props;
    const params = new URLSearchParams(location.search);
    const daysOfWeek = [
      'Monday',
      'Tuesday',
      'Wednesday',
      'Thursday',
      'Friday',
      'Saturday',
      'Sunday'
    ];
    const times = [
      '8am',
      '9am',
      '10am',
      '11am',
      '12pm',
      '1pm',
      '2pm',
      '3pm',
      '4pm',
      '5pm',
      '6pm',
      '7pm',
      '8pm',
      '9pm'
    ];

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
              <>
                <div className="section-info">
                  Lecture section for {params.get('course')}
                  {params.get('year') && (
                    <div>
                      year: {params.get('year')}
                      <br />
                      semester: {params.get('semester')}
                      <br />
                      section: {params.get('sectionCode')}
                    </div>
                  )}
                </div>
                <div className="section-agenda">
                  Select Day:{' '}
                  <select
                    className="section-day"
                    ref="daySelect"
                    onChange={this.dayPicked}
                  >
                    {daysOfWeek.map(d => (
                      <option value={d} key={d}>
                        {d}
                      </option>
                    ))}
                  </select>
                  <div className="section-times">
                    {times.map(t => (
                      <div key={t}>{t}</div>
                    ))}
                  </div>
                  <OHContainer slotNum={14} />
                </div>
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
