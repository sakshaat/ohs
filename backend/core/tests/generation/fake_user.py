from core.domain.user import Instructor, Student
from core.tests.generation import fake


def fake_instructor(user_name=None) -> Instructor:
    return Instructor(
        fake.first_name(), fake.last_name(), user_name if user_name else fake.pystr()
    )


def fake_student() -> Student:
    return Student(fake.first_name(), fake.last_name(), fake.pystr())
