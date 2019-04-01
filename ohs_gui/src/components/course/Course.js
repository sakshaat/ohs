import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import shortid from 'shortid';
import { toast } from 'react-toastify';

import LectureSectionCard from '../dashboard/LectureSectionCard';
import { getProfClient } from '../utils/client';
import { GET_SECTION_FOR_COURSE } from '../utils/queries';
import { roles } from '../utils/constants';

import './Course.css';

const client = getProfClient();

class Course extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sections: []
    };

    this.updateSectionList = this.updateSectionList.bind(this);
    this.getSections = this.getSections.bind(this);
  }

  componentDidMount() {
    this.getSections();
  }

  getSections() {
    const {
      user,
      match: {
        params: { courseCode }
      }
    } = this.props;

    // query sectons for the particular course
    client
      .query({
        query: GET_SECTION_FOR_COURSE,
        variables: {
          courseCode,
          taughtBy: user.userName
        }
      })
      .then(res => this.updateSectionList(res.data.sections))
      .catch(
        toast('Unknown Error - Could not get course', {
          type: toast.TYPE.ERROR
        })
      );
  }

  updateSectionList(lst) {
    this.setState({ sections: lst });
  }

  render() {
    const { sections } = this.state;
    const {
      user,
      match: {
        params: { courseCode }
      }
    } = this.props;

    const isProf = user && user.role === roles.PROFESSOR;

    return (
      <div id="sections">
        <div className="container">
          <div className="row">
            <div className="header-cont col-10">
              {courseCode && <h1>{courseCode} Lecture Sections </h1>}
            </div>
            <div className="header-cont col-2">
              <i
                onClick={() => window.location.reload()}
                className="fa fa-refresh fa-3x"
                aria-hidden="true"
              />
            </div>
          </div>
        </div>

        {sections.map(s => (
          <LectureSectionCard verbose section={s} key={shortid.generate()} />
        ))}
        {courseCode && isProf && (
          <Link to={`/course/${courseCode}/add-section`}>
            <div className="add-section card-element">
              <span className="fa fa-plus" />
            </div>
          </Link>
        )}
      </div>
    );
  }
}

export default Course;
