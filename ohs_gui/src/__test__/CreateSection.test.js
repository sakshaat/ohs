import Section from "../components/CreateSection"
import React from 'react';
import ReactTestUtils from 'react-dom/test-utils'; // ES6
import renderer from 'react-test-renderer';

test('Test update course list extracts course codes', () => {
  let component = ReactTestUtils.renderIntoDocument(<Section />);

  const res = {
    data: {
      courses: [
        {courseCode: "asdf"},
        {courseCode: "qwerty"},
        {courseCode: "qewrtyuiop"},
        {courseCode: "abcdefg"}
      ]
    }
  };
  
  const expected = ["asdf", "qwerty", "qewrtyuiop", "abcdefg"];

  component.updateCourseList(res);
  component.forceUpdate();
  expect(component.state.courseList).toEqual(expected);
});
