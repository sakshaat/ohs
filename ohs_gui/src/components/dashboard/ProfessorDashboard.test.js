import React from 'react';
import { shallow } from 'enzyme';

import ProfessorDashboard from './ProfessorDashboard';

const COURSES = ['CSC302', 'CSC202'];

// need this to deal with randomly generated ids
jest.mock('shortid', () => {
  return {
    generate: jest.fn(() => 1)
  };
});

it('should render correctly with no props', () => {
  const t = () => {
    shallow(<ProfessorDashboard />);
  };
  expect(t).toThrow(Error);
});

it('test if it renders with params', () => {
  const component = shallow(<ProfessorDashboard courses={COURSES} />);
  expect(component).toMatchSnapshot();
});

it('test if it renders with empty list', () => {
  const component = shallow(<ProfessorDashboard courses={[]} />);
  expect(component).toMatchSnapshot();
});
