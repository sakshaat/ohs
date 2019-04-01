import React from 'react';
import shortid from 'shortid';
import PropTypes from 'prop-types';

import LectureSectionCard from './LectureSectionCard';

class StudentDashboard extends React.PureComponent {
  render() {
    const { sections } = this.props;
    return (
      <div id="sections">
        <h1>Current Courses</h1>
        {sections.map(s => (
          <LectureSectionCard section={s} key={shortid.generate()} />
        ))}
      </div>
    );
  }
}

StudentDashboard.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  sections: PropTypes.array.isRequired
};

export default StudentDashboard;
