import { roles } from './constants';

function userIsProf(user) {
  return user && user.role === roles.PROFESSOR;
}

function getSemesterCode(sem) {
  // assumption: summer courses are assumed to be full session
  switch (sem) {
    case 'SUMMER':
    case 'FULL_YEAR':
      return 'Y';
    case 'WINTER':
      return 'S';
    case 'FALL':
      return 'F';
    default:
      return '';
  }
}

export { userIsProf, getSemesterCode };
