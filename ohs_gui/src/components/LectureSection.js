import React, { Component } from 'react';

class LectureSection extends Component {
  render() {
    return (
      <div>LectureSection: {this.props.match && this.props.match.params.id}</div>
    );
  }
}

export default LectureSection;
