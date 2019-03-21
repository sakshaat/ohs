import React, { Component } from 'react';

class MeetingComment extends Component {
  render() {
    const myComment = this.props.comment.author === this.props.user.first_name + ' ' + this.props.user.last_name;
    const dateFormat = require("dateformat")

    return (
      <div className={myComment ? "meeting-comment mine" : "meeting-comment theirs"}>
        <div className="comment-box">
          <p className="comment-content">
            {this.props.comment.contents}
          </p>
          <p className="comment-date">
            {dateFormat(new Date(this.props.comment.time), "mmmm dS, yyyy, h:MM TT")}
          </p>
        </div>
      </div>
    );
  }
}

export default MeetingComment;
