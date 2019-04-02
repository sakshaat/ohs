import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import gql from 'graphql-tag';
import { toast } from 'react-toastify';
import { Mutation } from 'react-apollo';

import { Button, FormGroup, FormControl } from 'react-bootstrap';

import './CreateSection.css';

const ADD_SECTION = gql`
  mutation addSection($sectionInput: SectionInput!) {
    createSection(sectionInput: $sectionInput) {
      sectionCode
    }
  }
`;
class CreateSection extends Component {
  constructor(props) {
    super(props);

    this.state = {
      sectionCreated: false,
      lsVal: '',
      yearVal: '',
      semesterVal: 'WINTER',
      snumVal: ''
    };
  }

  render() {
    const {
      sectionCreated,
      pickedCourse,
      lsVal,
      yearVal,
      semesterVal,
      snumVal
    } = this.state;

    const {
      user: { id },
      match: {
        params: { courseCode }
      }
    } = this.props;

    // variable
    const sectionInput = {
      course: { courseCode },
      year: yearVal,
      semester: semesterVal,
      sectionCode: lsVal,
      numStudents: snumVal,
      taughtBy: id
    };

    if (sectionCreated) {
      return <Redirect to={`/course/${courseCode}`} />;
    }

    const sectionComponent = (
      <div>
        <h1>Add a new Section to {pickedCourse}</h1>
        <FormGroup role="form">
          <FormControl
            ref="lsInput"
            placeholder="Section"
            aria-label="Section"
            aria-describedby="basic-addon2"
            onChange={e => this.setState({ lsVal: e.target.value })}
          />

          <FormControl
            ref="yearInput"
            placeholder="Year"
            aria-label="Year"
            aria-describedby="basic-addon2"
            type="number"
            onChange={e => this.setState({ yearVal: e.target.value })}
          />

          <FormControl
            ref="studentInput"
            placeholder="student"
            aria-label="student"
            aria-describedby="basic-addon2"
            type="number"
            onChange={e => this.setState({ snumVal: e.target.value })}
          />

          <select
            ref="semesterSelect"
            onChange={e => this.setState({ semesterVal: e.target.value })}
          >
            <option value="WINTER">WINTER</option>
            <option value="FALL">FALL</option>
            <option value="SUMMER">SUMMER</option>
            <option value="FULL_YEAR">FULL_YEAR</option>
          </select>

          <br />

          {lsVal && yearVal && semesterVal && snumVal && (
            <Mutation
              mutation={ADD_SECTION}
              variables={{ sectionInput }}
              options={{
                refetchQueries: ['getCourses']
              }}
              onCompleted={() => {
                this.setState({ sectionCreated: true });
                toast('New Section Created', {
                  type: toast.TYPE.SUCCESS
                });
              }}
              onError={() => {
                toast('Unknown Error - Could not create new section', {
                  type: toast.TYPE.ERROR
                });
              }}
            >
              {(mut, { loading }) => {
                return (
                  <div>
                    {loading && <p>Loading...</p>}
                    <Button variant="secondary" onClick={mut}>
                      Create a Section
                    </Button>
                  </div>
                );
              }}
            </Mutation>
          )}
        </FormGroup>
      </div>
    );

    return <section className="container">{sectionComponent}</section>;
  }
}

export default CreateSection;
