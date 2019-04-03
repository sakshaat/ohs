import React, { PureComponent } from 'react';
import { Button } from 'react-bootstrap';

// TO DO - Change this to import to be consistent
const dateFormat = require('dateformat');

class MeetingInfo extends PureComponent {
  render() {
    console.log(this.props);
    const { meeting, isProf, postponeMeeting, cancelMeeting } = this.props;

    return (
      <div className="meeting-info">
        {meeting && (
          <>
            <h2>Meeting with {isProf ? `${meeting.instructor.firstName} ${meeting.instructor.lastName}` : `${meeting.student.firstName} ${meeting.student.lastName}`}</h2>
            {dateFormat(new Date(meeting.startTime), 'mmmm dS, yyyy, h:MM TT')}
            <Button
              className="postpone-meeting"
              variant="warning"
              onClick={()=>postponeMeeting}
            >
              I&apos;m Running Late
            </Button>
            <Button
              className="cancel-meeting"
              variant="danger"
              onClick={()=>cancelMeeting(meeting.meetingId)}
            >
              Cancel Meeting
            </Button>
          </>
        )}
      </div>
    );
  }
}

export default MeetingInfo;
