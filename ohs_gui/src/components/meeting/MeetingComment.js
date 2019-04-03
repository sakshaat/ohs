import React, { PureComponent } from 'react';

// TO DO - Change this to import to be consistent
const dateFormat = require('dateformat');

class MeetingComment extends PureComponent {
  render() {
    const { comment, user } = this.props;
    
    let myComment;
    if(user.firstName === comment.author.firstName && user.firstName === comment.author.lastName) {
      myComment = false;
    } else {
      myComment = true;
    }

    return (
      <div
        className={
          myComment ? 'meeting-comment mine' : 'meeting-comment theirs'
        }
      >
        <div className="comment-box">
          <p className="comment-content">{comment.contentText}</p>
          <p className="comment-date">
            {dateFormat(new Date(comment.timeStamp), 'mmmm dS, yyyy, h:MM TT')}
          </p>
        </div>
      </div>
    );
  }
}

export default MeetingComment;
