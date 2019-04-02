import React from 'react';
import { shallow } from 'enzyme';
import { BrowserRouter as Router } from 'react-router-dom';
import { render, cleanup } from 'react-testing-library';
import { MockedProvider } from 'react-apollo/test-utils';

import { STUDENT_USER, PROF_USER } from '../utils/testUtils';

import Course from './Course';

import queryMock from '../utils/queryMock';

beforeEach(() => {
  // Make sure no mocks stick around between tests
  queryMock.reset();
});

// Clean up any mounted DOM by react-testing-library
afterEach(cleanup);

const MATCH = { params: { courseCode: 'CSC302' } };

it('should warn correctly with user prop only', () => {
  const t = () =>
    shallow(
      <MockedProvider>
        <Course user={STUDENT_USER} />
      </MockedProvider>
    );
  expect(t).toThrow(Error);
});

it('should warn correctly with match prop only', () => {
  const t = () =>
    shallow(
      <MockedProvider>
        <Course match={MATCH} />
      </MockedProvider>
    );
  expect(t).toThrow(Error);
});

it('renders course name', () => {
  const { getByText } = render(
    <MockedProvider>
      <Router>
        <Course user={PROF_USER} match={MATCH} />
      </Router>
    </MockedProvider>
  );
  expect(
    getByText(`${MATCH.params.courseCode} Lecture Sections`)
  ).toBeDefined();
});

it('check if it prof renders properly', () => {
  const component = shallow(
    <MockedProvider>
      <Course user={PROF_USER} match={MATCH} />
    </MockedProvider>
  );
  expect(component).toMatchSnapshot();
});

it('check if it student renders properly', () => {
  const component = shallow(
    <MockedProvider>
      <Course user={STUDENT_USER} match={MATCH} />
    </MockedProvider>
  );
  expect(component).toMatchSnapshot();
});

// it('mock getting new sections', async () => {
//   // intercept http requests
//   queryMock.mockQuery({
//     name: 'getSectionForCourse',
//     data: {
//       sections: SECTIONS
//     },
//     variables: {
//       courseCode: MATCH.params.courseCode,
//       taughtBy: PROF_USER.userName
//     }
//   });

//   const wrapper = shallow(<MockedProvider><Course user={PROF_USER} match={MATCH} /></MockedProvider>);
//   wrapper.update();
//   expect(wrapper.state('sections').length).toEqual(2);
// });
