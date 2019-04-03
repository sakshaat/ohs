import gql from 'graphql-tag';

const GET_COURSES = gql`
  query getCourses {
    courses {
      courseCode
    }
  }
`;

const ENROLL_STUDENTS = gql`
  mutation enrollStudents($sectionInput: SectionInput!, $studentNumbers: [String]!) {
    enrollStudents(sectionInput: $sectionInput, studentNumbers: $studentNumbers) {
      studentNumbers
    }
  }
`;

  const GET_MEETING = gql`
  query getMeeting($meetingId: UUID!) {
    meeting(meetingId: $meetingId) {
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
          ... on Student {
            studentNumber
            firstName
            lastName
          }
          ... on Instructor {
            userName
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
          ... on Student {
            studentNumber
            firstName
            lastName
          }
          ... on Instructor {
            userName
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

const CREATE_COMMENT = gql`
  mutation createComment($meetingId: UUID!, $contentText: String!) {
    createComment(meetingId: $meetingId, contentText: $contentText) {
            commentId
            meetingId
            author {
                ... on Instructor {
                    userName
                }
                ... on Student {
                    studentNumber
                }
            }
            timeStamp
            contentText
        }
    }
`;

const CREATE_NOTE = gql`
    mutation createNote($meetingId: UUID!, $contentText: String!) {
        createNote(meetingId: $meetingId, contentText: $contentText) {
            noteId
            meetingId
            timeStamp
            contentText
        }
    }
`;

const DELETE_NOTE = gql`
    mutation deleteNote($noteId: UUID!) {
        deleteNote(noteId: $noteId,) {
            noteId
        }
    }
`;

const DELETE_MEETING = gql`
    mutation deleteMeeting($meetingId: UUID!) {
        deleteMeeting(meetingId: $meetingId,) {
            meetingId
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
  GET_MEETING,
  GET_OFFICE_HOURS_BY_SECTION_AND_WEEKDAY,
  ENROLL_STUDENTS,
  CREATE_COMMENT,
  CREATE_NOTE,
  DELETE_NOTE,
  DELETE_MEETING,
};
