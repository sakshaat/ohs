import React from 'react';
import { shallow } from 'enzyme';

import MeetingCard from './MeetingCard';

// const MEETING = {
//     meetingId: 1,
//     officeHourId: 2,
//     index: 5,
//     instructor: {
//         firstName: "Albert",
//         lastName: "Einstein",
//         userName: "emc2"
//     },
//     student: {
//         firstName: "Bernie",
//         lastName: "Sanders",
//         studentNumber: 245
//     },
//     notes: [],
//     comments: [],
//     startTime: 100
// }

it('should render correctly with no props', () => {
  const t = () => {
    shallow(<MeetingCard />);
  };
  expect(t).toThrow(Error);
});

// it('test if it renders with params', () => {
//     const component = shallow(<MeetingCard meeting={MEETING} isProf/>);
//     expect(component).toMatchSnapshot();
// });

// it('test if it renders with empty list', () => {
//     const component = shallow(<MeetingCard meeting={MEETING}/>);
//     expect(component).toMatchSnapshot();
// });
