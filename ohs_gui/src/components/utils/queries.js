import gql from 'graphql-tag';

const GET_COURSES = gql`
  {
    courses {
      courseCode
    }
  }
`;

const GET_SECTIONS = gql`
  {
    sections {
      course {
        courseCode
      }
      year
      semester
      sectionCode
    }
  }
`;

const GET_SECTION = gql`
  query getSection(
    $course: CourseInput!
    $year: Int!
    $semester: Semester!
    $sectionCode: String!
  ) {
    section(
      course: $course
      year: $year
      semester: $semester
      sectionCode: $sectionCode
    ) {
      course {
        courseCode
      }
      year
      semester
      sectionCode
      numStudents
    }
  }
`;

const GET_SECTION_FOR_COURSE = gql`
  query getSectionForCourse($courseCode: String!, $taughtBy: String!) {
    sections(courseCode: $courseCode, taughtBy: $taughtBy) {
      course {
        courseCode
      }
      year
      semester
      sectionCode
      numStudents
    }
  }
`;

export { GET_COURSES, GET_SECTIONS, GET_SECTION, GET_SECTION_FOR_COURSE };
