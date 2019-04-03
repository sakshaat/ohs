import React, { Component } from 'react';
import OHContainer from '../officeHours/OHContainer';

class CreateOfficeHours extends Component {
  constructor(props) {
    super(props);

    this.state = {
      bookedSlots: []
    };

    this.toggleBooking = this.toggleBooking.bind(this);
    this.changeDay = this.changeDay.bind(this);
    this.getOH = this.getOH.bind(this);

    this.selectDay = React.createRef();
    this.slotNum = 14; // number of times per day where we can book office hours
  }

  componentDidMount() {
    this.getOH('Monday');
  }

  getOH(day) {
    console.log(day);
    // TODO: dummy json - get office hours
    const bookedSlots = new Array(this.slotNum);
    for (let i = 0; i < bookedSlots.length; i += 1) {
      bookedSlots[i] = false;
    }

    this.setState({ bookedSlots });
  }

  changeDay() {
    const val = this.selectDay.current.value;
    this.getOH(val);
  }

  toggleBooking(idx) {
    const { bookedSlots } = this.state;
    const lst = bookedSlots.slice(0);
    let consent = false;
    if (lst[idx]) {
      consent = window.confirm(
        'Are you sure you want to delete this office hour?'
      );
    } else {
      consent = window.confirm(
        'Are you sure you want to create an office hour in this timeslot?'
      );
    }

    if (consent) {
      // TODO: update office hours in backend
      // negate that index
      lst[idx] = !lst[idx];
      this.setState({ bookedSlots: lst });
    }
  }

  render() {
    const { bookedSlots } = this.state;
    const daysOfWeek = [
      'Monday',
      'Tuesday',
      'Wednesday',
      'Thursday',
      'Friday',
      'Saturday',
      'Sunday'
    ];
    const times = [
      '8am',
      '9am',
      '10am',
      '11am',
      '12pm',
      '1pm',
      '2pm',
      '3pm',
      '4pm',
      '5pm',
      '6pm',
      '7pm',
      '8pm',
      '9pm'
    ];

    return (
      <div className="section-agenda">
        Select Day:{' '}
        <select
          className="section-day"
          ref={this.selectDay}
          onChange={this.changeDay}
        >
          {daysOfWeek.map(d => (
            <option value={d} key={d}>
              {d}
            </option>
          ))}
        </select>
        <div className="section-times">
          {times.map(t => (
            <div key={t}>{t}</div>
          ))}
        </div>
        <div className="create-office-hours">
          <OHContainer
            bookedSlots={bookedSlots}
            toggleBooking={this.toggleBooking}
            showBooked={false}
          />
        </div>
      </div>
    );
  }
}

export default CreateOfficeHours;
