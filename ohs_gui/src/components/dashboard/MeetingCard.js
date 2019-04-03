import React, { PureComponent } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

const dateFormat = require('dateformat');

class MeetingCard extends PureComponent {
  render() {
    const { meeting, isProf } = this.props;
    
    return (
      <Link to={`/meeting/${meeting.meetingId}`} state={{meeting}}>
        <div className="meeting card-element">
          {dateFormat(new Date(meeting.startTime), 'mmmm dS, yyyy, h:MM TT')}
          <br />
          <div>Meeting with </div>{isProf ? `${meeting.instructor.firstName} ${meeting.instructor.lastName}` : `${meeting.student.firstName} ${meeting.student.lastName}`}
        </div>
      </Link>
    );
  }
}

MeetingCard.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  meeting: PropTypes.object.isRequired,
  isProf: PropTypes.bool.isRequired
};

export default MeetingCard;
