from unittest.mock import MagicMock

import pytest
from option import Some

from common.tests.generation.fake_course import fake_course, fake_section
from instructor_service.presistence.course_persistence import CoursePresistence


@pytest.fixture()
def course_presistence() -> CoursePresistence:
    return CoursePresistence()


class TestCreateCourse:
    def test_success(self, course_presistence):
        course = fake_course()
        assert course_presistence.create_course(course).unwrap() == course
        assert course_presistence.get_course(course.course_code).unwrap() == course

    def test_duplicate(self, course_presistence):
        course = fake_course()
        course_presistence.get_course = MagicMock(return_value=Some(course))
        assert (
            course_presistence.create_course(course).unwrap_err()
            == f"Course {course} already exists"
        )


class TestCreateSection:
    def test_success(self, course_presistence):
        section = fake_section()
        course_presistence.get_course = MagicMock(return_value=Some(section.course))
        assert course_presistence.create_section(section).unwrap() == section
        assert course_presistence.get_section(section.section_code).unwrap() == section

    def test_invalid_course(self, course_presistence):
        section = fake_section()
        assert (
            course_presistence.create_section(section).unwrap_err()
            == f"Course {section.course} does not exist"
        )
        assert course_presistence.get_section(section.section_code).is_none

    def test_duplicate(self, course_presistence):
        section = fake_section()
        course_presistence.get_section = MagicMock(return_value=Some(section))
        assert (
            course_presistence.create_section(section).unwrap_err()
            == f"Section {section} already exists"
        )
