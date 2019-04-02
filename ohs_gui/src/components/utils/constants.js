// User roles
const roles = {
  PROFESSOR: 1,
  STUDENT: 2
};

const PROF_BASE_URL = `${process.env.REACT_APP_INSTRUCTOR_SERVICE_URL ||
  'http://localhost:8000'}`;

const STUDENT_BASE_URL = `${process.env.REACT_APP_STUDENT_SERVICE_URL ||
  'http://localhost:8001'}`;

// helper
const roleLabels = n => (n === roles.PROFESSOR ? 'Professor' : 'Student');

export { roles, roleLabels, PROF_BASE_URL, STUDENT_BASE_URL };
