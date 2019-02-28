from unittest.mock import MagicMock

import pytest
from option import NONE, Some

from common.domain.course import Course
from common.tests.generation import fake, list_fakes
from common.tests.generation.fake_course import fake_course
from instructor_service.api.course_api import CourseApi
from instructor_service.gql.context import InstructorContext
from instructor_service.gql.graphql_schema import schema


@pytest.fixture()
def mock_context():
    mock_context = MagicMock(InstructorContext)
    mock_course_api = MagicMock(CourseApi)
    mock_context.api.course_api = mock_course_api
    return mock_context, mock_course_api


@pytest.fixture
def course_query():
    return """
query getCourse($courseCode: String!) {
    course(courseCode: $courseCode) {
        courseCode
    }
}"""


@pytest.fixture
def courses_query():
    return """
query queryCourses($filters: String) {
    courses(filters: $filters) {
        courseCode
    }
}"""


def test_query_course(course_query, mock_context):
    course_code = fake.pystr()
    mock_context, mock_course_api = mock_context
    mock_course_api.get_course = MagicMock(return_value=Some(Course(course_code)))
    result = schema.execute(
        course_query, variables={"courseCode": course_code}, context=mock_context
    )
    assert result.data == {"course": {"courseCode": course_code}}
    mock_course_api.get_course.assert_called_once_with(course_code)


def test_query_course_not_found(course_query, mock_context):
    course_code = fake.pystr()
    mock_context, mock_course_api = mock_context
    mock_course_api.get_course = MagicMock(return_value=NONE)
    result = schema.execute(
        course_query, variables={"courseCode": course_code}, context=mock_context
    )
    assert result.data == {"course": None}
    mock_course_api.get_course.assert_called_once_with(course_code)


@pytest.mark.parametrize("filters", [None, fake.pystr()])  # TODO: Use actual filters
@pytest.mark.parametrize("num_courses", [0, 10])
def test_query_courses(courses_query, mock_context, filters, num_courses):
    courses = list_fakes(fake_course, num_courses)
    mock_context, mock_course_api = mock_context
    mock_course_api.query_courses = MagicMock(return_value=courses)
    variables = {"filters": filters} if filters else None
    result = schema.execute(courses_query, variables=variables, context=mock_context)
    assert result.data == {
        "courses": [{"courseCode": course.course_code} for course in courses]
    }
    mock_course_api.query_courses.assert_called_once_with(filters)
