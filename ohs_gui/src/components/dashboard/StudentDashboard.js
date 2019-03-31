import React from 'react';
import shortid from 'shortid';
import LectureSectionCard from './LectureSectionCard';

class StudentDashboard extends React.PureComponent {
  render() {
    const { sections } = this.props;
    return (
      <div id="sections">
        <h1>Current Courses</h1>
        {sections.map(s => (
          <LectureSectionCard verbose section={s} key={shortid.generate()} />
        ))}
      </div>
    );
  }
}

export default StudentDashboard;
