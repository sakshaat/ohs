// User roles
const roles = {
  PROFESSOR: 1,
  STUDENT: 2
};

// helper
const roleLabels = n => (n === roles.PROFESSOR ? 'Professor' : 'Student');

export { roles, roleLabels };
