import React, { PureComponent } from 'react';

// TO DO - Change this to import to be consistent
const dateFormat = require('dateformat');

class MeetingComment extends PureComponent {
  render() {
    const { comment, user } = this.props;
    const myComment = comment.author === `${user.first_name} ${user.last_name}`;

    return (
      <div
        className={
          myComment ? 'meeting-comment mine' : 'meeting-comment theirs'
        }
      >
        <div className="comment-box">
          <p className="comment-content">{comment.contents}</p>
          <p className="comment-date">
            {dateFormat(new Date(comment.time), 'mmmm dS, yyyy, h:MM TT')}
          </p>
        </div>
      </div>
    );
  }
}

export default MeetingComment;
