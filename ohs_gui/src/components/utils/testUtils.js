import { roles } from './constants';

const PROF_USER = {
  firstName: 'Albert',
  lastName: 'Einstein',
  role: roles.PROFESSOR,
  userName: 'emc2'
};

const STUDENT_USER = {
  firstName: 'Bernie',
  lastName: 'Sanders',
  role: roles.STUDENT,
  userName: 'sensan'
};

const SECTIONS = [
  {
    course: {
      courseCode: 'CSC302'
    },
    year: 2019,
    semester: 'FALL',
    sectionCode: 'LEC0101',
    numStudents: 25
  },
  {
    course: {
      courseCode: 'CSC304'
    },
    year: 2019,
    semester: 'FALL',
    sectionCode: 'LEC0102',
    numStudents: 25
  }
];

export { SECTIONS, PROF_USER, STUDENT_USER };
