import React, { Component } from 'react';
import gql from 'graphql-tag';
import { toast } from 'react-toastify';
import { Query, Mutation } from 'react-apollo';
import OHContainer from '../officeHours/OHContainer';
import { GET_OFFICE_HOURS_BY_SECTION_AND_WEEKDAY } from '../utils/queries';


const ADD_OH = gql`
mutation createOfficeHour($sectionInput: SectionInput!, $startingHour: Int!, $weekday: Weekday!) {
  createOfficeHour(sectionInput: $sectionInput, startingHour: $startingHour, weekday: $weekday) {
    officeHourId
    section {
      sectionCode
    }
    startingHour
    weekday
    meetings {
      meeting {
        meetingId
      }
    }
  }
}`;

const DELETE_OH = gql`
mutation deleteOfficeHour($officeHourId: UUID!) {
  deleteOfficeHour(officeHourId: $officeHourId) {
    officeHourId
  }
}`;

class CreateOfficeHours extends Component {
  constructor(props) {
    super(props);

    this.state = {
      day: "MONDAY",
      newOHTime: null,
      deleteOHId: null
    };

    this.toggleBooking = this.toggleBooking.bind(this);
    this.changeDay = this.changeDay.bind(this);

    this.selectDay = React.createRef();
    this.slotNum = 14; // number of times per day where we can book office hours
  }

  changeDay() {
    const val = this.selectDay.current.value;
    this.setState({day: val})
  }

  toggleBooking(idx, booked) {
    if (booked) {
      if (window.confirm(
        'Are you sure you want to delete this office hour?'
      )) {
        let id = null
        if (this.officehours){
          this.officehours.forEach(elem => {
            if (elem.startingHour === idx + 8){
              id = elem.officeHourId;
            }
          });
        }
        this.setState({deleteOHId: id});
      }
    } else if (window.confirm(
        'Are you sure you want to create an office hour in this timeslot?'
      )) {
        this.setState({newOHTime: idx + 8})
      }
  }

  render() {
    const { section } = this.props;
    const { day, newOHTime, deleteOHId } = this.state;
    const daysOfWeek = [
      'MONDAY',
      'TUESDAY',
      'WEDNESDAY',
      'THURSDAY',
      'FRIDAY',
      'SATURDAY',
      'SUNDAY'
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
    const variables = {
      "sectionInput": {
        "course": {"courseCode": section.course.courseCode},
        "year": section.year,
        "semester": section.semester,
        "sectionCode": section.sectionCode,
        "numStudents": section.numStudents,
        "taughtBy": section.taughtBy.userName
      },
	    "weekday": day
    }
    const mutVariables = {
      "sectionInput": {
        "course": {"courseCode": section.course.courseCode},
        "year": section.year,
        "semester": section.semester,
        "sectionCode": section.sectionCode,
        "numStudents": section.numStudents,
        "taughtBy": section.taughtBy.userName
      },
	    "weekday": day,
      "startingHour": newOHTime
    }
    
    return (
      <Mutation
        mutation={DELETE_OH}
        variables={{"officeHourId": deleteOHId}}
        update={(cache, response) => {
          const addr = { query: GET_OFFICE_HOURS_BY_SECTION_AND_WEEKDAY, variables };
          const data = cache.readQuery(addr);
          data.officehours = data.officehours.filter(elem => {
              return elem.officeHourId !== response.data.deleteOfficeHour.officeHourId
          });
          cache.writeQuery({...addr, data});
        }}
        onCompleted={() => {
          toast('Office Hour Deleted', {
            type: toast.TYPE.SUCCESS
          });
        }}
        onError={() => {
          toast('Unknown Error - Could not delete office hour', {
            type: toast.TYPE.ERROR
          });
        }}
      >
        {(mut) => {
          if(deleteOHId){
            this.setState({ deleteOHId: null });
            mut();
          }
          return (
            <Mutation
              mutation={ADD_OH}
              variables={mutVariables}
              update={(cache, response) => {
                const addr = { query: GET_OFFICE_HOURS_BY_SECTION_AND_WEEKDAY, variables };
                const data = cache.readQuery(addr);
                data.officehours.push(response.data.createOfficeHour);
                cache.writeQuery({...addr, data});
              }}
              onCompleted={() => {
                toast('New Office Hour Created', {
                  type: toast.TYPE.SUCCESS
                });
              }}
              onError={() => {
                toast('Unknown Error - Could not create new office hour', {
                  type: toast.TYPE.ERROR
                });
              }}
            >
              {(newMut) => {
                if(newOHTime){
                  this.setState({ newOHTime: null });
                  newMut();
                }
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
                    <Query
                      query={GET_OFFICE_HOURS_BY_SECTION_AND_WEEKDAY}
                      variables={variables}
                      onError={() => {
                        toast('Unknown Error - Could not get office hours', {
                          type: toast.TYPE.ERROR
                        });
                      }}
                    >
                      {({ data }) => {
                        const { officehours } = data;
                        this.officehours = officehours;
                        if (officehours) {
                          const bookedSlots = new Array(this.slotNum);
                          for (let i = 0; i < bookedSlots.length; i += 1) {
                            bookedSlots[i] = false;
                          }
                          officehours.forEach((elem) => {
                            bookedSlots[elem.startingHour - 8] = true;
                          });
                          return (
                            <OHContainer
                              bookedSlots={bookedSlots}
                              toggleBooking={this.toggleBooking}
                              showBooked={false}
                            />
                          );
                        }
                        return null;
                        }}
                      </Query>
                    </div>
                  </div>
                );
              }}
            </Mutation>
                );
        }}
      </Mutation>
    );
  }
}

export default CreateOfficeHours;
