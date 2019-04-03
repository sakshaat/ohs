import React, { PureComponent } from 'react';
import { Button } from 'react-bootstrap';

// TO DO - Change this to import to be consistent
const dateFormat = require('dateformat');

class MeetingInfo extends PureComponent {
  render() {
    const { meeting, isProf, postponeMeeting, cancelMeeting } = this.props;

    return (
      <div className="meeting-info">
        {meeting && (
          <>
            <h2>Meeting With {isProf ? meeting.student : meeting.professor}</h2>
            Course: {meeting.courseCode}
            <br />
            {dateFormat(new Date(meeting.time), 'mmmm dS, yyyy, h:MM TT')}
            <br />
            {meeting.room}
            <Button
              className="postpone-meeting"
              variant="warning"
              onClick={postponeMeeting}
            >
              I&apos;m Running Late
            </Button>
            <Button
              className="cancel-meeting"
              variant="danger"
              onClick={cancelMeeting(meeting.meetingId)}
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
