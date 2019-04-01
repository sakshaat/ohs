import React from 'react';
import { shallow } from 'enzyme';

import StudentDashboard from './StudentDashboard';

const SECTIONS = [
  {
    course: {
      courseCode: 'CSC302'
    },
    year: 2019,
    semester: 'FALL',
    sectionCode: 'LEC0101',
    numStudent: 25
  },
  {
    course: {
      courseCode: 'CSC304'
    },
    year: 2019,
    semester: 'FALL',
    sectionCode: 'LEC0102',
    numStudent: 25
  }
];

// need this to deal with randomly generated ids
jest.mock('shortid', () => {
  return {
    generate: jest.fn(() => 1)
  };
});

it('should render correctly with no props', () => {
  const t = () => {
    shallow(<StudentDashboard />);
  };
  expect(t).toThrow(Error);
});

it('test if it renders with params', () => {
  const component = shallow(<StudentDashboard sections={SECTIONS} />);
  expect(component).toMatchSnapshot();
});

it('test if it renders with empty list', () => {
  const component = shallow(<StudentDashboard sections={[]} />);
  expect(component).toMatchSnapshot();
});
