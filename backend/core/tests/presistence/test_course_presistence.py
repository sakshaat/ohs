from unittest.mock import MagicMock

import pytest
from option import Some
import os
import psycopg2

from core.tests.generation.fake_course import fake_course, fake_section
from core.presistence.course_persistence import CoursePresistence


@pytest.fixture()
def course_presistence() -> CoursePresistence:
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_DBHOST"),
        dbname=os.getenv("POSTGRES_DBNAME"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    yield CoursePresistence(lambda: conn)
    conn.close()


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
        assert course_presistence.get_section(section.identity).unwrap() == section

    def test_invalid_course(self, course_presistence):
        section = fake_section()
        assert (
            course_presistence.create_section(section).unwrap_err()
            == f"Course {section.course} does not exist"
        )
        assert course_presistence.get_section(section.identity).is_none

    def test_duplicate(self, course_presistence):
        section = fake_section()
        course_presistence.get_section = MagicMock(return_value=Some(section))
        assert (
            course_presistence.create_section(section).unwrap_err()
            == f"Section {section} already exists"
        )
