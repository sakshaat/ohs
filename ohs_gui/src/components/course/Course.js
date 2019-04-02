/* eslint-disable react/forbid-prop-types */
import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import shortid from 'shortid';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import { Query } from 'react-apollo';

import LectureSectionCard from '../dashboard/LectureSectionCard';
import { GET_SECTIONS_FOR_COURSE } from '../utils/queries';
import { roles } from '../utils/constants';

import './Course.css';

class Course extends Component {
  render() {
    const {
      user,
      match: {
        params: { courseCode }
      }
    } = this.props;

    const isProf = user && user.role === roles.PROFESSOR;
    const variables = {
      courseCode,
      taughtBy: user.userName
    };

    return (
      <div id="sections">
        <div className="container">
          <div className="row">
            <div className="header-cont col-10">
              {courseCode && <h1>{courseCode} Lecture Sections</h1>}
            </div>
          </div>
        </div>

        <Query
          query={GET_SECTIONS_FOR_COURSE}
          variables={variables}
          onError={() => {
            toast('Unknown Error - Could not get sections for the course', {
              type: toast.TYPE.ERROR
            });
          }}
        >
          {({ data }) => {
            if (data) {
              const { sections } = data;
              if (sections) {
                const lst = sections.map(s => (
                  <LectureSectionCard
                    verbose
                    section={s}
                    key={shortid.generate()}
                  />
                ));
                return lst;
              }
            }

            return null;
          }}
        </Query>

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

Course.propTypes = {
  user: PropTypes.shape({
    firstName: PropTypes.string,
    lastName: PropTypes.string,
    userName: PropTypes.string,
    role: PropTypes.number
  }).isRequired,
  // eslint-disable-next-line react/require-default-props
  match: PropTypes.object.isRequired
};

export default Course;
