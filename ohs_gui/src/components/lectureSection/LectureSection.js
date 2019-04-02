import React, { Component } from 'react';
import { toast } from 'react-toastify';
import { Query } from 'react-apollo';

import { GET_SECTION } from '../utils/queries';
import { userIsProf, getSemesterCode } from '../utils/helpers';

import OHContainer from '../officeHours/OHContainer';
import './LectureSection.css';

class LectureSection extends Component {
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
    const { location, user } = this.props;
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

    const params = new URLSearchParams(location.search);
    const variables = {
      course: { courseCode: params.get('course') },
      year: params.get('year'),
      semester: params.get('semester'),
      sectionCode: params.get('sectionCode')
    };

    const isProf = userIsProf(user);

    const profAgenda = (
      <div className="section-agenda">
        Select Day:
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
        <OHContainer
          bookedSlots={bookedSlots}
          toggleBooking={this.toggleBooking}
        />
      </div>
    );

    const studentAgenda = <div className="section-agenda" />;

    return (
      <Query
        query={GET_SECTION}
        variables={variables}
        onError={() => {
          toast('Unknown Error - Could not find the section', {
            type: toast.TYPE.ERROR
          });
        }}
      >
        {({ data }) => {
          const { section } = data;
          if (section) {
            return (
              <>
                <div className="section-info">
                  <h1>
                    {`${section.course.courseCode}H1${getSemesterCode(
                      section.semester
                    )} - ${section.sectionCode}`}
                  </h1>
                  <div>
                    year: {section.year}
                    <br />
                    number of students: {section.numStudents}
                  </div>
                </div>
                {isProf ? profAgenda : studentAgenda}
              </>
            );
          }
          return null;
        }}
      </Query>
    );
  }
}

export default LectureSection;
