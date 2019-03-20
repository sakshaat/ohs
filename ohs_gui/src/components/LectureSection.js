import React, { Component } from 'react';

class LectureSection extends Component {
  render() {
    let params = new URLSearchParams(this.props.location.search);

    return (
      <div>
        LectureSection for {params.get("course")}
        {params.get("year") && (
          <div>
            year: {params.get("year")}
            <br />
            semester: {params.get("semester")}
            <br />
            section_code: {params.get("section_code")}
          </div>
        )}
      </div>
    );
  }
}

export default LectureSection;
