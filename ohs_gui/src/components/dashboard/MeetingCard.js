import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class MeetingCard extends Component {
  render() {
    const dateFormat = require("dateformat")
    return (
      <Link to={`/meeting/${this.props.meeting.id}`}>
        <div className="meeting card-element">
          {this.props.meeting.courseCode}
          <br />
          {dateFormat(new Date(this.props.meeting.time), "mmmm dS, yyyy, h:MM TT")}
          <br />
          {this.props.meeting.room}
          <br />
          {this.props.isProf ?
            this.props.meeting.student : this.props.meeting.professor}
        </div>
      </Link>
    );
  }
}

export default MeetingCard;
