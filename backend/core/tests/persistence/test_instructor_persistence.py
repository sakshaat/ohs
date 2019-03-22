from unittest.mock import MagicMock

import pytest
from option import Some
import os
import psycopg2

from core.tests.generation.fake_user import fake_instructor
from core.persistence.instructor_persistence import InstructorPersistence


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


class TestCreateInstructor:
    def test_success(self, instructor_persistence):
        instructor = fake_instructor()
        assert (
            instructor_persistence.create_instructor(instructor, "aaaa").unwrap()
            == instructor
        )
        assert (
            instructor_persistence.get_instructor(instructor.user_name).unwrap()
            == instructor
        )
        assert (
            instructor_persistence.get_password_hash(instructor.user_name).unwrap()
            == "aaaa"
        )
        instructor_persistence.delete_instructor(instructor)

    def test_duplicate(self, instructor_persistence):
        instructor = fake_instructor()
        instructor_persistence.get_instructor = MagicMock(return_value=Some(instructor))
        assert (
            instructor_persistence.create_instructor(instructor, "aaaa").unwrap_err()
            == f"Instructor {instructor} already exists"
        )

    def test_update_hash(self, instructor_persistence):
        instructor = fake_instructor()
        instructor_persistence.create_instructor(instructor, "aaaa")
        assert (
            instructor_persistence.get_password_hash(instructor.user_name).unwrap()
            == "aaaa"
        )
        assert (
            instructor_persistence.update_password_hash(
                instructor.user_name, "bbbb"
            ).unwrap()
            is None
        )
        assert (
            instructor_persistence.get_password_hash(instructor.user_name).unwrap()
            == "bbbb"
        )
        instructor_persistence.delete_instructor(instructor)
