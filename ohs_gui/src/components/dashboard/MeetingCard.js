import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class MeetingCard extends Component {
  render() {
    const dateFormat = require("dateformat")
    return (
      <Link to={`/meeting/${this.props.meeting.id}`}>
        <div className={this.props.verbose ? "meeting-verbose card-element" : "meeting card-element"}>
          {this.props.meeting.courseCode}
          <br />
          {dateFormat(new Date(this.props.meeting.time), "mmmm dS, yyyy, h:MM TT")}
          <br />
          {this.props.meeting.room}
          <br />
          {this.props.verbose &&
            this.props.meeting.bookedBy}
        </div>
      </Link>
    );
  }
}

export default MeetingCard;
