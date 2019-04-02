import gql from 'graphql-tag';

const GET_COURSES = gql`
  query getCourses {
    courses {
      courseCode
    }
  }
`;

  const GET_MEETINGS = gql`
  query getMeeting($meetingId: String!) {
    meeting(meetingId: $meetingId) {
    meeting_id
    office_hour_id
    index
    instructor
    student
    notes
    comments
    start_time
    }
  }
`;

const GET_UPCOMING_MEETINGS = gql`
  query getUpcomingMeetings {
    upcomingMeetings {
      meetingId
      officeHourId
      index
      instructor {
        firstName
        lastName
        userName
      }
      student {
        firstName
        lastName
        studentNumber
      }
      startTime
    }
  }
`;

const GET_SECTIONS = gql`
  query getSections {
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

const GET_SECTIONS_FOR_STUDENT = gql`
  query getSectionForStudent($studentNum: String!) {
    sections(enrolledIn: $studentNum) {
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

const GET_SECTIONS_FOR_COURSE = gql`
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

export {
  GET_COURSES,
  GET_SECTIONS,
  GET_SECTION,
  GET_SECTIONS_FOR_COURSE,
  GET_UPCOMING_MEETINGS,
  GET_SECTIONS_FOR_STUDENT,
  GET_MEETINGS
};
