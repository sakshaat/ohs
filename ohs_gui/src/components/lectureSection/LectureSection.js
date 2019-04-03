import React, { PureComponent } from 'react';
import { toast } from 'react-toastify';
import { Query } from 'react-apollo';
import { Redirect } from 'react-router-dom';
import { Button } from 'react-bootstrap';

import CreateOfficeHours from './CreateOfficeHours';
import BookMeetings from './BookMeetings';

import { GET_SECTION } from '../utils/queries';
import { userIsProf, getFormattedSectionName } from '../utils/helpers';

import './LectureSection.css';

class LectureSection extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      redirectToAddStudents: false
    };
  }

  render() {
    const { location, user } = this.props;
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

    const isProf = userIsProf(user);

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
              <>
                <div className="section-info">
                  <h1>{getFormattedSectionName(section)}</h1>
                  <div>number of students: {section.numStudents}</div>
                  {isProf ? 
                  <Button

                  className="add-btn"
                    onClick={() =>
                      this.setState({ redirectToAddStudents: true })
                    }
                  >
                    Add Students
                  </Button>:
                null}
                  
                </div>
                {isProf ? <CreateOfficeHours section={section} /> : <BookMeetings section={section} />}
              </>
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
