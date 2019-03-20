import React, { Component } from 'react';
import MeetingNote from './meeting/MeetingNote';
import MeetingComment from './meeting/MeetingComment';
import ReactDOM from 'react-dom'
import { Button, FormGroup, FormControl } from 'react-bootstrap';

import "./Meeting.css"

class Meeting extends Component {
  constructor(props) {
    super(props);
    this.state = {
      meeting: null,
      notes: [],
      comments: []
    }

    this.getMeeting = this.getMeeting.bind(this);
    this.getNotes = this.getNotes.bind(this);
    this.getComments = this.getComments.bind(this);
    this.createComment = this.createComment.bind(this);
  }

  componentDidMount() {
    const isProf = this.props.user && this.props.user.role === "PROFESSOR";

    this.getMeeting();
    this.getComments();
    if (isProf) {
      this.getNotes();
    }
  }

  getMeeting() {
    // TODO: dummy json
    // fetch meeting using this.props.match.params.id
    const meeting = {
      time: "2019-11-17T17:15:00.000Z",
      room: "BA1234",
      courseCode: "CSC302H1S",
      bookedBy: "Pikachu",
      id: 11
    }
    this.setState({ meeting: meeting })
  }

  getNotes() {
    // TODO: dummy json
    const notes = [
      {
        time: "2019-11-17T17:15:00.000Z",
        contents: "I choose you, Pikachu"
      },
      {
        time: "2019-11-17T17:18:00.000Z",
        contents: "haha this student is a fat electric mouse"
      }
    ]
    this.setState({ notes: notes })
  }

  getComments() {
    // TODO: dummy json
    const comments = [
      {
        time: "2019-11-17T17:15:00.000Z",
        contents: "Hello, Pikachu",
        author: "AlecGibson"
      },
      {
        time: "2019-11-17T17:16:00.000Z",
        contents: "PIKA",
        author: "Pikachu"
      },
      {
        time: "2019-11-17T17:16:30.000Z",
        contents: "Is that all you can say?",
        author: "AlecGibson"
      },
      {
        time: "2019-11-17T17:18:00.000Z",
        contents: "PIKA",
        author: "Pikachu"
      },
      {
        time: "2019-11-17T17:20:00.000Z",
        contents: "Well this is gonna be an eventful meeting...",
        author: "AlecGibson"
      }
    ]
    this.setState({ comments: comments })
  }

  createComment() {
    // TODO: add comment to backend
    const comment = {
      time: new Date().toISOString(),
      contents: ReactDOM.findDOMNode(this.refs.commentInput).value,
      author: this.props.user.first_name + this.props.user.last_name
    }
    console.log(comment)
    const comments = this.state.comments;
    comments.push(comment)
    console.log(comments)
    this.setState({ comments: comments })
    ReactDOM.findDOMNode(this.refs.commentInput).value = "";
  }

  render() {
    const isProf = this.props.user && this.props.user.role === "PROFESSOR";

    return (
      <div>
        <div className="meeting-main">
          <div className="meeting-info">
            <h2>Meeting Info:</h2>
          </div>
          <div className="meeting-comments">
            <h2>Comments</h2>
            {this.state.comments.map(c => (
              <MeetingComment comment={c} user={this.props.user} />
            ))}
          </div>
          <div className="new-comment">
            <FormGroup role="form">

              <FormControl ref="commentInput"
                placeholder="New comment"
                aria-label="Comment"
                aria-describedby="basic-addon2"
              />

              <Button variant="primary" onClick={this.createComment}>Submit</Button>
            </FormGroup>
          </div>
        </div>
        {isProf &&
          <div className="meeting-notes">
            <h2>Notes</h2>
            {this.state.notes.map(n => (
              <MeetingNote note={n} />
            ))}
          </div>
        }
      </div>
    );
  }
}

export default Meeting;
