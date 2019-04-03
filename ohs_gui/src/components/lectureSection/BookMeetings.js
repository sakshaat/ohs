import React, { Component } from 'react';
import * as Datetime from 'react-datetime';
import * as moment from 'moment';
import OHContainer from '../officeHours/OHContainer';

class BookMeetings extends Component {
  constructor(props) {
    super(props);

    this.state = {
      date: '',
      officeHours: []
    };

    this.dateChange = this.dateChange.bind(this);
    this.toggleBooking = this.toggleBooking.bind(this);
  }

  dateChange(date) {
    // TODO: query backend for all office hours and their corresponding meetings
    const officeHours = [
      {
        startTime: moment('2019-04-16T15:00:00.000Z').format('h:mm'),
        meetings: [true, true, false, true, false, true]
      },
      {
        startTime: moment('2019-04-16T18:00:00.000Z').format('h:mm'),
        meetings: [false, true, true, true, false, false]
      }
    ];

    this.setState({ date, officeHours });
  }

  toggleBooking(startTime) {
    // TODO: backend integration
    // TODO: after creating meeting in backend, force sidebar to reload
    return function(idx) {
      const { officeHours } = this.state;

      let ohIdx = null;
      officeHours.forEach(function(oh, i) {
        if (oh.startTime === startTime) {
          ohIdx = i;
        }
      });

      const lst = officeHours.slice(0);
      let consent = false;
      if (!lst[ohIdx].meetings[idx]) {
        consent = window.confirm(
          'Are you sure you want to book a meeting in this timeslot?'
        );
      }

      if (consent) {
        // TODO: update office hours in backend
        // negate that index
        lst[ohIdx].meetings[idx] = !lst[ohIdx].meetings[idx];
        this.setState({ officeHours: lst });
      }
    }.bind(this);
  }

  render() {
    const { date, officeHours } = this.state;
    return (
      <div className="section-agenda">
        Date:{' '}
        <Datetime
          inputProps={{ placeholder: 'Select a date' }}
          dateFormat="MM-DD-YYYY"
          timeFormat={false}
          onChange={this.dateChange}
        />
        <br />
        <br />
        {officeHours.length !== 0 && (
          <h2>Book a meeting on {moment(date).format('MMMM Do')}</h2>
        )}
        <div className="office-hours">
          {officeHours.map(oh => (
            <div className="office-hour" key={oh.startTime}>
              <p className="start-time">{oh.startTime}</p>
              <div className="slots">
                <OHContainer
                  bookedSlots={oh.meetings}
                  toggleBooking={this.toggleBooking(oh.startTime)}
                  showBooked
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }
}

export default BookMeetings;
