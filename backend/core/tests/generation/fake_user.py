from core.domain.user import Instructor, Student
from core.tests.generation import fake


def fake_instructor() -> Instructor:
    return Instructor(fake.first_name(), fake.last_name(), fake.sha256(), fake.pystr())


def fake_student() -> Student:
    return Student(fake.first_name(), fake.last_name(), fake.sha256(), fake.py_str())
