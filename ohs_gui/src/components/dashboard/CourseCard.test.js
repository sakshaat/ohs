import React from 'react';
import { shallow } from 'enzyme';
import { Link } from 'react-router-dom';

import CourseCard from './CourseCard';

const COURSE = 'CSC302';

it('should render correctly with no props', () => {
  const t = () => {
    shallow(<CourseCard />);
  };
  expect(t).toThrow(Error);
});

it('renders course name', () => {
  const component = shallow(<CourseCard course={COURSE} />);
  const text = component.find('.course').text();
  expect(text).toEqual(COURSE);
});

it('check if it renders properly', () => {
  const component = shallow(<CourseCard course={COURSE} />);
  expect(component).toMatchSnapshot();
});

it('test if Link is created to the right URL', () => {
  const component = shallow(<CourseCard course={COURSE} />);
  const link = component.find(Link).prop('to');
  expect(link).toEqual(`/course/${COURSE}`);
});
