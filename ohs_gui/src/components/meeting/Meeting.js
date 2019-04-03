/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable jsx-a11y/aria-role */
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { withRouter } from 'react-router-dom';
import { Button, FormGroup, FormControl, Modal } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { Query, Mutation } from 'react-apollo';

import MeetingNote from './MeetingNote';
import MeetingComment from './MeetingComment';
import MeetingInfo from './MeetingInfo';

import { userIsProf } from '../utils/helpers';

import {
    GET_MEETING,
    CREATE_COMMENT,
    CREATE_NOTE
} from '../utils/queries';

import './Meeting.css';

class Meeting extends Component {
  constructor(props) {
    super(props);
    const { user } = this.props;

    this.state = {
      notes: [],
      comments: [],
      show: false,
      showNotes: user && user.role === 'PROFESSOR',
      contentText: "",
      noteText: ""
    };    


    this.handleClose = this.handleClose.bind(this);
    this.handleShow = this.handleShow.bind(this);
    this.addNote = this.addNote.bind(this);
    this.removeNote = this.removeNote.bind(this);
    this.cancelMeeting = this.cancelMeeting.bind(this);
    this.postponeMeeting = this.postponeMeeting.bind(this);
    this.minimizeNotes = this.minimizeNotes.bind(this);
    this.expandNotes = this.expandNotes.bind(this);
  }

  contentChanged = (e) => {
    this.setState({contentText: e.target.value});
  }

  noteTextChange = (e) => {
    this.setState({noteText: e.target.value});
  }

  oldCreateComment() {
    // TODO: add comment to backend
    if (ReactDOM.findDOMNode(this.refs.commentInput).value === '') {
      return;
    }

    const { user } = this.props;

    const comment = {
      time: new Date().toISOString(),
      contents: ReactDOM.findDOMNode(this.refs.commentInput).value,
      author: user.first_name + user.last_name
    };
    const { comments } = this.state;
    comments.push(comment);
    this.setState({ comments });
    ReactDOM.findDOMNode(this.refs.commentInput).value = '';
  }

 /* CreateComment() {
    // TODO: add comment to backend
    if (ReactDOM.findDOMNode(this.refs.commentInput).value === '') {
      return;
    }

    const { user } = this.props;
    const {comments} = this.state;
return (
    <Mutation
      mutation={CREATE_COMMENT}
      variables={{commentInput: {meetingId: meetingId, contentText: contentText}}}
       onCompleted={() => {
        this.setState({ courseCreated: true });
        toast('New Course Created', {
            type: toast.TYPE.SUCCESS
          });
        }}
       onError={() => {
        toast('Unknown Error - Could not create new course', {
            type: toast.TYPE.ERROR
        });
       }}
    >
    </Mutation>
  );
}; */


  handleClose() {
    this.setState({ show: false });
  }

  handleShow() {
    this.setState({ show: true });
  }

  scrollToBottom() {
    if (this.bottom) {
      this.bottom.scrollIntoView({ behavior: 'smooth' });
    }
  }

  addNote() {
    // TODO: add note to backend
    const note = {
      time: new Date().toISOString(),
      contents: ReactDOM.findDOMNode(this.refs.noteInput).value
    };
    const { notes } = this.state;
    notes.push(note);
    this.setState({ notes });
    ReactDOM.findDOMNode(this.refs.noteInput).value = '';
    this.setState({ show: false });
  }


  cancelMeeting(meetingId) {
    console.log(meetingId, this);

    // if (window.confirm('Are you sure you want to cancel this meeting?')) {
    //    return(<Mutation mutation={DELETE_MEETING} variables={{meetingId}}
    //    onCompleted={ () => {

    //    }}
    //    >
    //    </Mutation>
    //    // TODO: redirect out of meeting into courses page
    //    );
    // }
  }

  postponeMeeting() {
    // TODO: delay meeting in backend
    if (window.confirm('Are you sure you want to postpone this meeting?')) {
      const { meeting } = this.state;
      const time = new Date(meeting.time);
      time.setTime(time.getTime() + 1000 * 60 * 60);
      meeting.time = time.toISOString();
      this.setState({ meeting });
    }
  }

  minimizeNotes(e) {
    const elem = e.target;
    let pos = 0;
    const id = setInterval(
      function() {
        if (pos === 400) {
          clearInterval(id);
          this.setState({ showNotes: false });
        } else {
          pos += 20;
          elem.style.left = `${pos}px`;
        }
      }.bind(this),
      5
    );
  }

  expandNotes() {
    this.setState({ showNotes: true });
  }

  render() {
    const {
      user,
      match: {
        params: { id }
      }
    } = this.props;

    console.log(id);

    const isProf = userIsProf(user);

    const { notes, show, showNotes, contentText, noteText } = this.state;

    return (
      <>
         <Query
          query={GET_MEETING}
          variables={{meetingId: id}}
          onError={() => {
            toast('Unknown Error - Could not get meeting', {
              type: toast.TYPE.ERROR
            });
          }}
        >{({ data }) => {
           if (data) {
              const { meeting } = data;
              if (meeting) {
               return(
       <>
        <div className={showNotes ? 'meeting-main' : 'meeting-main-full'}>
          <MeetingInfo
            meeting={meeting}
            isProf={isProf}
            cancelMeeting={this.cancelMeeting}
            postponeMeeting={this.postponeMeeting}
          />
          <div className="meeting-comments">
            <h2>Comments</h2>
            {meeting.comments.map(c => (
              <MeetingComment key={c.time + c.author} comment={c} user={user} />
            ))}
            <div
              ref={bottom => {
                this.bottom = bottom;
              }}
            />
          </div>
          <div className="new-comment">


          <form onSubmit={e => this.createComment(e)}>
            <FormGroup role="form">
              <FormControl
                ref="commentInput"
                placeholder="New comment"
                aria-label="Comment"
                aria-describedby="basic-addon2"
                onChange={this.contentChanged}
              />
              <Mutation mutation={CREATE_COMMENT} variables={{meetingId:id, contentText}} >
              {(createComment) => {

              return (<Button variant="primary" onClick={createComment}>
                Submit
              </Button>
              );
              }}
              </Mutation>
            </FormGroup>

           </form>
          </div>
        </div>
        {isProf && showNotes && (
          <div className="meeting-notes" ref="notes" role="presenation" onClick={this.minimizeNotes}>
            <h2>Notes</h2>
            <span
              className="minimize-notes fa fa-chevron-right"
              role="presentation"
            />
            {meeting.notes.map(n => (
              <MeetingNote key={n.time} note={n} removeNote={this.removeNote} />
            ))}
            <Button variant="primary" onClick={this.handleShow}>
              Add Note
            </Button>
          </div>
        )}
        {isProf && !showNotes && (
          <div
            className="expand-notes fa fa-chevron-left"
            onClick={this.expandNotes}
            role="presentation"
          />
        )}
        <Modal show={show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Add Note</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <textarea onChange={this.noteTextChange} className="note-input" ref="noteInput" />
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={this.handleClose}>
              Close
            </Button>
            <Mutation mutation={CREATE_NOTE} variables={{id, noteText}}>
            {(createNote) => {
            this.setState({notes: notes.push(createNote)});
            return(
            <Button variant="primary" onClick={createNote}>
              Save
            </Button>
            );
            }}
            </Mutation>
          </Modal.Footer>
        </Modal>
       </>
       );
       }
       }
         return null;
        }}
        </Query>
        
      </>
    );
  }
}

export default withRouter(Meeting);
