import React, { PureComponent } from 'react';
// TO DO use import to stay consistent
const dateFormat = require('dateformat');

class MeetingNote extends PureComponent {
  render() {
    const { removeNote, note } = this.props;
    return (
      <div className="meeting-note">
        <span
          className="note-delete"
          role="presentation"
          onClick={removeNote(note.noteId)}
        >
          &#10006;
        </span>
        <p className="note-date">
          {dateFormat(new Date(note.time), 'mmmm dS, yyyy, h:MM TT')}
        </p>
        <p className="note-content">{note.content}</p>
      </div>
    );
  }
}

export default MeetingNote;
