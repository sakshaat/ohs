import React, { Component } from 'react';

class MeetingNote extends Component {
  render() {
    const dateFormat = require("dateformat")

    return (
      <div className="meeting-note">
        <span className="note-delete" onClick={this.props.removeNote(this.props.note.time)}>&#10006;</span>
        <p className="note-date">
          {dateFormat(new Date(this.props.note.time), "mmmm dS, yyyy, h:MM TT")}
        </p>
        <p className="note-content">
          {this.props.note.contents}
        </p>
      </div>
    );
  }
}

export default MeetingNote;
