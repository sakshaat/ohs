import gql from "graphql-tag";

const GET_COURSES = gql`{
    courses {
      courseCode
    }
  }`;

const GET_SECTIONS = gql`{
    sections {
      course {
        courseCode
      }
      year
      semester
      sectionCode
    }
  }`;

export {GET_COURSES, GET_SECTIONS}