import gql from 'graphql-tag';

const GET_COURSES = gql`
  query getCourses {
    courses {
      courseCode
    }
  }
`;

  const GET_MEETINGS = gql`
  query getMeeting($meetingId: UUID!) {
    meeting(meetingId: $meetingId) {
        meetingId
        officeHourId
        index
        instructor {
            userName
            firstName
            lastName
        }
        student {
            studentNumber
            firstName
            lastName
        }
        notes {
            noteId
            meetingId
            timeStamp
            contentText
        }
        comments {
            commentId
            meetingId
            author {
                ... on Instructor {
                    userName
                    firstName
                    lastName
                }
                ... on Student {
                    studentNumber
                    firstName
                    lastName
                }
            }
            timeStamp
            contentText
        }
        startTime
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
      taughtBy {
        userName
      }
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

const GET_OFFICE_HOURS_BY_SECTION_AND_WEEKDAY = gql`
  query getOfficeHours($sectionInput: SectionInput!, $weekday: Weekday!) {
    officehours(sectionInput: $sectionInput, weekday: $weekday) {
      officeHourId
      startingHour
      weekday
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
  GET_MEETINGS,
  GET_OFFICE_HOURS_BY_SECTION_AND_WEEKDAY
};
