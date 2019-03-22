from unittest.mock import MagicMock

import pytest
from option import Some
import os
import psycopg2

from core.tests.generation.fake_user import fake_student
from core.persistence.student_persistence import StudentPersistence


@pytest.fixture()
def student_persistence() -> StudentPersistence:
    conn = psycopg2.connect(
        host=os.getenv("OHS_DB_HOST"),
        dbname=os.getenv("OHS_DB_NAME"),
        user=os.getenv("OHS_DB_USER"),
        password=os.getenv("OHS_DB_PASSWORD"),
    )
    yield StudentPersistence(lambda: conn)
    conn.close()


class TestCreateStudent:
    def test_success(self, student_persistence):
        student = fake_student()
        assert student_persistence.create_student(student, "aaaa").unwrap() == student
        assert (
            student_persistence.get_student(student.student_number).unwrap() == student
        )
        assert (
            student_persistence.get_password_hash(student.student_number).unwrap()
            == "aaaa"
        )
        student_persistence.delete_student(student)

    def test_duplicate(self, student_persistence):
        student = fake_student()
        student_persistence.get_student = MagicMock(return_value=Some(student))
        assert (
            student_persistence.create_student(student, "aaaa").unwrap_err()
            == f"Student {student} already exists"
        )

    def test_update_hash(self, student_persistence):
        student = fake_student()
        student_persistence.create_student(student, "aaaa")
        assert (
            student_persistence.get_password_hash(student.student_number).unwrap()
            == "aaaa"
        )
        assert (
            student_persistence.update_password_hash(
                student.student_number, "bbbb"
            ).unwrap()
            is None
        )
        assert (
            student_persistence.get_password_hash(student.student_number).unwrap()
            == "bbbb"
        )
        student_persistence.delete_student(student)
