import React from 'react';
import { shallow } from 'enzyme';

import StudentDashboard from './StudentDashboard';
import { SECTIONS } from '../utils/testUtils';

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
