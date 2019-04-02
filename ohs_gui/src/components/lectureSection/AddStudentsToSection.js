import React, { PureComponent } from 'react';
import TagsInput from 'react-tagsinput';
import { Button } from 'react-bootstrap';

import 'react-tagsinput/react-tagsinput.css';

class AddStudentsToSection extends PureComponent {
  constructor(props) {
    super(props);
    this.state = { tags: [] };

    this.tagChange = this.tagChange.bind(this);
    this.addBtnClicked = this.addBtnClicked.bind(this);
  }

  addBtnClicked() {
    console.log(this.state);
  }

  tagChange(tags) {
    this.setState({ tags });
  }

  render() {
    const { location } = this.props;
    const params = new URLSearchParams(location.search);

    const { tags } = this.state;

    const variables = {
      course: { courseCode: params.get('course') },
      year: params.get('year'),
      semester: params.get('semester'),
      sectionCode: params.get('sectionCode')
    };

    return (
      <div>
        <h1>Add Students</h1>
        <h3>{`${variables.course.courseCode} - ${variables.sectionCode} (${
          variables.semester
        } ${variables.year})`}</h3>
        <TagsInput value={tags} onChange={this.tagChange} />

        <Button onClick={this.addBtnClicked}>Add Students</Button>
      </div>
    );
  }
}

export default AddStudentsToSection;
