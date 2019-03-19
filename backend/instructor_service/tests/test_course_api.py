from unittest.mock import MagicMock

import pytest
from option import Err, NONE, Ok, Some

from core.tests.generation import fake, list_fakes
from core.tests.generation.fake_course import fake_course, fake_section
from instructor_service.api.course_api import CourseApi
from instructor_service.presistence.course_persistence import CoursePresistence


@pytest.fixture()
def mock_course_presistence():
    return MagicMock(CoursePresistence)


class TestCreateSection:
    def test_success(self, mock_course_presistence):
        course_api = CourseApi(mock_course_presistence)
        section = fake_section()
        mock_course_presistence.create_section = MagicMock(return_value=Ok(section))
        assert (
            course_api.create_section(
                section.course,
                section.year,
                section.semester,
                section.section_code,
                section.taught_by,
                section.num_students,
            ).unwrap()
            == section
        )
        mock_course_presistence.create_section.assert_called_once_with(section)

    def test_fail(self, mock_course_presistence):
        course_api = CourseApi(mock_course_presistence)
        section = fake_section()
        err = Err(fake.pystr())
        mock_course_presistence.create_section = MagicMock(return_value=err)
        assert (
            course_api.create_section(
                section.course,
                section.year,
                section.semester,
                section.section_code,
                section.taught_by,
                section.num_students,
            )
            == err
        )
        mock_course_presistence.create_section.assert_called_once_with(section)


class TestCreateCourse:
    def test_success(self, mock_course_presistence):
        course_api = CourseApi(mock_course_presistence)
        course = fake_course()
        mock_course_presistence.create_course = MagicMock(return_value=Ok(course))
        assert course_api.create_course(course.course_code).unwrap() == course
        mock_course_presistence.create_course.assert_called_once_with(course)

    def test_fail(self, mock_course_presistence):
        course_api = CourseApi(mock_course_presistence)
        course = fake_course()
        err = Err(fake.pystr())
        mock_course_presistence.create_course = MagicMock(return_value=err)
        assert course_api.create_course(course.course_code) == err
        mock_course_presistence.create_course.assert_called_once_with(course)


@pytest.mark.parametrize("filters,expected", [(None, list_fakes(fake_course, 5))])
def test_query_courses(mock_course_presistence, filters, expected):
    course_api = CourseApi(mock_course_presistence)
    mock_course_presistence.query_courses = MagicMock(return_value=expected)
    assert course_api.query_courses(filters) == expected
    mock_course_presistence.query_courses.assert_called_once_with(filters)


@pytest.mark.parametrize("filters,expected", [(None, list_fakes(fake_section, 5))])
def test_query_sections(mock_course_presistence, filters, expected):
    course_api = CourseApi(mock_course_presistence)
    mock_course_presistence.query_sections = MagicMock(return_value=expected)
    assert course_api.query_sections(filters) == expected
    mock_course_presistence.query_sections.assert_called_once_with(filters)


@pytest.mark.parametrize("expected", [NONE, Some(fake_course())])
def test_get_course(mock_course_presistence, expected):
    course_api = CourseApi(mock_course_presistence)
    mock_course_presistence.get_course = MagicMock(return_value=expected)
    course_code = expected.map_or(lambda c: c.course_code, None)
    assert course_api.get_course(course_code) == expected
    mock_course_presistence.get_course.assert_called_once_with(course_code)


@pytest.mark.parametrize("expected", [NONE, Some(fake_section())])
def test_get_section(mock_course_presistence, expected):
    course_api = CourseApi(mock_course_presistence)
    expected_identity = expected.map_or(lambda section: section.identity, None)
    mock_course_presistence.get_section = MagicMock(return_value=expected)
    assert course_api.get_section(expected_identity) == expected
    mock_course_presistence.get_section.assert_called_once_with(expected_identity)
