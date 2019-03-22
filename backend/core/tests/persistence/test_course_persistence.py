from unittest.mock import MagicMock

import pytest
from option import Some
import os
import psycopg2

from core.tests.generation.fake_course import fake_course, fake_section
from core.persistence.course_persistence import CoursePersistence
from core.persistence.instructor_persistence import InstructorPersistence


@pytest.fixture()
def course_persistence() -> CoursePersistence:
    conn = psycopg2.connect(
        host=os.getenv("OHS_DB_HOST"),
        dbname=os.getenv("OHS_DB_NAME"),
        user=os.getenv("OHS_DB_USER"),
        password=os.getenv("OHS_DB_PASSWORD"),
    )
    yield CoursePersistence(lambda: conn)
    conn.close()


@pytest.fixture()
def instructor_persistence() -> InstructorPersistence:
    conn = psycopg2.connect(
        host=os.getenv("OHS_DB_HOST"),
        dbname=os.getenv("OHS_DB_NAME"),
        user=os.getenv("OHS_DB_USER"),
        password=os.getenv("OHS_DB_PASSWORD"),
    )
    yield InstructorPersistence(lambda: conn)
    conn.close()


class TestCreateCourse:
    def test_success(self, course_persistence):
        course = fake_course()
        assert course_persistence.create_course(course).unwrap() == course
        assert course_persistence.get_course(course.course_code).unwrap() == course
        course_persistence.delete_course(course.course_code)

    def test_duplicate(self, course_persistence):
        course = fake_course()
        course_persistence.get_course = MagicMock(return_value=Some(course))
        assert (
            course_persistence.create_course(course).unwrap_err()
            == f"Course {course} already exists"
        )


class TestCreateSection:
    def test_success(self, course_persistence, instructor_persistence):
        section = fake_section()
        course_persistence.create_course(section.course)
        instructor_persistence.create_instructor(section.taught_by, "aaaaa")
        assert course_persistence.create_section(section).unwrap() == section
        assert course_persistence.get_section(section.identity).unwrap() == section
        course_persistence.delete_section(section.identity)
        course_persistence.delete_course(section.course.course_code)
        instructor_persistence.delete_instructor(section.taught_by)

    def test_invalid_course(self, course_persistence):
        section = fake_section()
        assert (
            course_persistence.create_section(section).unwrap_err()
            == f"Course {section.course} does not exist"
        )
        assert course_persistence.get_section(section.identity).is_none

    def test_duplicate(self, course_persistence):
        section = fake_section()
        course_persistence.get_section = MagicMock(return_value=Some(section))
        assert (
            course_persistence.create_section(section).unwrap_err()
            == f"Section {section} already exists"
        )
