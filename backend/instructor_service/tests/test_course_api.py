from unittest.mock import MagicMock

import pytest
from option import Err, Ok

from common.tests.generation import fake
from common.tests.generation.fake_course import fake_course, fake_section
from instructor_service.api.course_api import CourseApi
from instructor_service.db.course_persistence import CoursePresistence


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
                section.session,
                section.section_code,
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
                section.session,
                section.section_code,
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
