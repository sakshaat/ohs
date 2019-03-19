from uuid import uuid4

from common.domain.user import Instructor, Student
from common.tests.generation import fake


def fake_instructor() -> Instructor:
    return Instructor(uuid4(), fake.first_name(), fake.last_name(), fake.sha256())


def fake_student() -> Student:
    return Student(
        uuid4(), fake.first_name(), fake.last_name(), fake.sha256(), fake.py_str()
    )
