import React, { Component } from 'react';

class Meeting extends Component {
  render() {
    const dateFormat = require("dateformat")
    return (
      <div className="meeting card-element">
        {this.props.meeting.courseCode}
        <br />
        {dateFormat(new Date(this.props.meeting.time), "mmmm dS, yyyy, h:MM TT")}
        <br />
        {this.props.meeting.room}
      </div>
    );
  }
}

export default Meeting;
