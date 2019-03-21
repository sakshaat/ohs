import React, { Component } from 'react';
import { Button } from 'react-bootstrap';

class MeetingInfo extends Component {
  render() {
    const dateFormat = require("dateformat")
    const { meeting, isProf } = this.props

    return (
      <div className="meeting-info">
        {meeting &&
          <>
            <h2>Meeting With {isProf ? meeting.student : meeting.professor}</h2>
            Course: {meeting.courseCode}
            <br />
            {dateFormat(new Date(meeting.time), "mmmm dS, yyyy, h:MM TT")}
            <br />
            {meeting.room}
            <Button className="postpone-meeting" variant="warning" onClick={this.props.postponeMeeting}>I'm Running Late</Button>
            <Button className="cancel-meeting" variant="danger" onClick={this.props.cancelMeeting}>Cancel Meeting</Button>
          </>
        }
      </div>
    );
  }
}

export default MeetingInfo;
