import React, { Component } from 'react';

class LectureSection extends Component {
  render() {
    return (
      <div className="lecture-section card-element">
        {this.props.section.courseCode}
      </div>
    );
  }
}

export default LectureSection;
