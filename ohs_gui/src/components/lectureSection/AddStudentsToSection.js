import React, { PureComponent } from 'react';
import TagsInput from 'react-tagsinput';
import { Button } from 'react-bootstrap';
import {Redirect} from 'react-router-dom';

import 'react-tagsinput/react-tagsinput.css';
import {Query, Mutation} from "react-apollo";
import {toast} from "react-toastify";

import {GET_SECTION, ENROLL_STUDENTS} from "../utils/queries";
import {userIsProf} from "../utils/helpers"


class AddStudentsToSection extends PureComponent {
  constructor(props) {
    super(props);
    this.state = { tags: [], studentsEnrolled : false };

    this.tagChange = this.tagChange.bind(this);

  }

  tagChange(tags) {
    this.setState({ tags });
  }

  render() {
      
    const { location, user } = this.props;
    const params = new URLSearchParams(location.search);

    const { tags, studentsEnrolled } = this.state;

    const variables = {
      course: { courseCode: params.get('course') },
      year: params.get('year'),
      semester: params.get('semester'),
      sectionCode: params.get('sectionCode')
    };

    if(!userIsProf(user) || studentsEnrolled) {
        return <Redirect to="/" />
    }

    return (
      <div>
        <h1>Add Students</h1>
        <h3>{`${variables.course.courseCode} - ${variables.sectionCode} (${
          variables.semester
        } ${variables.year})`}</h3>
        <TagsInput value={tags} onChange={this.tagChange} />

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
            // variables
            const sectionInput = {
                course: { courseCode: section.course.courseCode },
                year: section.year,
                semester: section.semester,
                sectionCode: section.sectionCode,
                numStudents: section.numStudents,
                taughtBy: section.taughtBy
              };
            
            return (

            <Mutation
                mutation={ENROLL_STUDENTS}
                variables={{ sectionInput, studentNumbers: tags}}
                onCompleted={() => {
                    this.setState({ studentsEnrolled: true });
                    toast('Students Enrolled', {
                        type: toast.TYPE.SUCCESS
                    });
                }}
                onError={() => {
                    toast('Unknown Error - Could not add students', {
                        type: toast.TYPE.ERROR
                    });
                }}
                >
                {(mut, { loading }) => {
                    return (
                    <div>
                        {loading && <p>Loading...</p>}
                        <Button onClick={mut}>Add Students</Button>
                    </div>
                    );
                }}
            </Mutation>
                
            );
          }
          return null;
          }}
        </Query>

        
      </div>
    );
  }
}

export default AddStudentsToSection;
