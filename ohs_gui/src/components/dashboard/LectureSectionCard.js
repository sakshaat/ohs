import React, { PureComponent } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { getFormattedSectionName } from '../utils/helpers';

class LectureSectionCard extends PureComponent {
  render() {
    const { section } = this.props;
    return (
      <Link
        to={{
          pathname: '/section',
          search: `?course=${section.course.courseCode}&year=${
            section.year
          }&semester=${section.semester}&sectionCode=${section.sectionCode}`
        }}
      >
        <div className="card-element lecture-section">
          <div>{getFormattedSectionName(section)}</div>
        </div>
      </Link>
    );
  }
}

LectureSectionCard.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  section: PropTypes.object.isRequired
};

export default LectureSectionCard;
