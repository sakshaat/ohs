import React from 'react';
import { shallow } from 'enzyme';

import LectureSectionCard from './LectureSectionCard';

const SECTION = {
  course: {
    courseCode: 'CSC302'
  },
  year: 2019,
  semester: 'FALL',
  sectionCode: 'LEC0101',
  numStudent: 25
};

it('should render correctly with no props', () => {
  const t = () => {
    shallow(<LectureSectionCard />);
  };
  expect(t).toThrow(Error);
});

it('test if it renders with params', () => {
  const component = shallow(<LectureSectionCard section={SECTION} />);
  expect(component).toMatchSnapshot();
});
