import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class LectureSection extends Component {
  render() {
    return (
      <Link to={`/lectureSection/${this.props.section.id}`}>
        <div className="lecture-section card-element">
          {this.props.section.courseCode}
        </div>
      </Link>
    );
  }
}

export default LectureSection;
