from unittest.mock import MagicMock

import pytest
from option import Err, Ok

from common.tests.generation import fake
from common.tests.generation.fake_course import fake_course, fake_section
from instructor_service.api.course_api import CourseApi
from instructor_service.gql.context import InstructorContext
from instructor_service.gql.graphql_schema import schema


@pytest.fixture()
def mock_context():
    context = MagicMock(InstructorContext)
    course_api = MagicMock(CourseApi)
    context.api.course_api = course_api
    return context, course_api


@pytest.fixture()
def create_course_query():
    return """
mutation createCourse($courseCode: String!) {
    createCourse(courseInput: {courseCode: $courseCode}) {
        courseCode
    }
}"""


def test_create_course(mock_context, create_course_query):
    context, course_api = mock_context
    course = fake_course()
    course_api.create_course = MagicMock(return_value=Ok(course))
    result = schema.execute(
        create_course_query,
        variables={"courseCode": course.course_code},
        context=context,
    )
    assert not result.errors
    assert result.data == {"createCourse": {"courseCode": course.course_code}}
    course_api.create_course.assert_called_once_with(course.course_code)


def test_create_course_fail(mock_context, create_course_query):
    context, course_api = mock_context
    course = fake_course()
    error = fake.pystr()
    course_api.create_course = MagicMock(return_value=Err(error))
    result = schema.execute(
        create_course_query,
        variables={"courseCode": course.course_code},
        context=context,
    )
    assert error in str(result.errors[0])
    course_api.create_course.assert_called_once_with(course.course_code)


@pytest.fixture()
def create_section_query():
    return """
mutation createSection($sectionInput: SectionInput!) {
    createSection(sectionInput: $sectionInput) {
        course {
            courseCode
        }
        year
        semester
        sectionCode
        numStudents
    }
}"""


def section_input(section):
    return {
        "sectionInput": {
            "course": {"courseCode": section.course.course_code},
            "year": section.year,
            "semester": section.semester.name,
            "numStudents": section.num_students,
            "sectionCode": section.section_code,
        }
    }


def test_create_section(mock_context, create_section_query):
    context, course_api = mock_context
    section = fake_section()
    course_api.create_section = MagicMock(return_value=Ok(section))
    result = schema.execute(
        create_section_query, variables=section_input(section), context=context
    )
    assert not result.errors
    assert result.data == {
        "createSection": {
            "course": {"courseCode": section.course.course_code},
            "year": section.year,
            "semester": section.semester.name,
            "numStudents": section.num_students,
            "sectionCode": section.section_code,
        }
    }
    course_api.create_section.assert_called_once_with(
        section.course,
        section.year,
        section.semester,
        section.section_code,
        section.num_students,
    )


def test_create_section_fail(mock_context, create_section_query):
    context, course_api = mock_context
    section = fake_section()
    error = fake.pystr()
    course_api.create_section = MagicMock(return_value=Err(error))
    result = schema.execute(
        create_section_query, variables=section_input(section), context=context
    )
    assert error in str(result.errors[0])
    course_api.create_section.assert_called_once_with(
        section.course,
        section.year,
        section.semester,
        section.section_code,
        section.num_students,
    )
