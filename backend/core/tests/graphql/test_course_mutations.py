from unittest.mock import MagicMock

import pytest
from option import Err, Ok, Some

from core.api.course_api import CourseApi
from core.api.instructor_api import InstructorApi
from core.gql.context import Context
from core.tests.generation import fake
from core.tests.generation.fake_course import fake_course, fake_section


@pytest.fixture()
def mock_context():
    context = MagicMock(Context)
    course_api = MagicMock(CourseApi)
    instructor_api = MagicMock(InstructorApi)
    context.api.course_api = course_api
    context.api.instructor_api = instructor_api
    context.user = None
    return context, course_api, instructor_api


@pytest.fixture()
def create_course_query():
    return """
mutation createCourse($courseCode: String!) {
    createCourse(courseInput: {courseCode: $courseCode}) {
        courseCode
    }
}"""


def test_create_course(schema, mock_context, create_course_query):
    context, course_api, instructor_api = mock_context
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


def test_create_course_fail(schema, mock_context, create_course_query):
    context, course_api, instructor_api = mock_context
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
        taughtBy {
            userName
            firstName
            lastName
        }
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


@pytest.mark.parametrize("supply_instructor", [True, False])
def test_create_section(schema, mock_context, create_section_query, supply_instructor):
    context, course_api, instructor_api = mock_context
    section = fake_section()

    if supply_instructor:
        instructor_api.get_instructor = MagicMock(return_value=Some(section.taught_by))
    else:
        context.user = section.taught_by

    course_api.create_section = MagicMock(return_value=Ok(section))
    variables = section_input(section)
    if supply_instructor:
        variables["sectionInput"]["taughtBy"] = section.taught_by.user_name
    result = schema.execute(create_section_query, variables=variables, context=context)
    assert not result.errors
    assert result.data == {
        "createSection": {
            "course": {"courseCode": section.course.course_code},
            "year": section.year,
            "semester": section.semester.name,
            "taughtBy": {
                "userName": section.taught_by.user_name,
                "firstName": section.taught_by.first_name,
                "lastName": section.taught_by.last_name,
            },
            "numStudents": section.num_students,
            "sectionCode": section.section_code,
        }
    }
    course_api.create_section.assert_called_once_with(
        section.course,
        section.year,
        section.semester,
        section.section_code,
        section.taught_by,
        section.num_students,
    )


def test_create_section_fail(schema, mock_context, create_section_query):
    context, course_api, instructor_api = mock_context
    section = fake_section()
    context.user = section.taught_by
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
        section.taught_by,
        section.num_students,
    )
