from random import choice
from uuid import uuid4

from core.domain.course import Course, OfficeHour, Section, Semester, Weekday
from core.tests.generation import fake
from core.tests.generation.fake_meeting import fake_meeting
from core.tests.generation.fake_user import fake_instructor


def fake_course() -> Course:
    course_code = fake.pystr()
    return Course(course_code)


def fake_section(course=None, year=None, semester=None) -> Section:
    course = course or fake_course()
    year = year or int(fake.year())
    semester = semester or choice(list(Semester))
    section_code = fake.pystr()
    instructor = fake_instructor()
    num_students = fake.pyint()
    return Section(course, year, semester, section_code, instructor, num_students)


def fake_officehour():
    return OfficeHour(
        uuid4(),
        fake_section(),
        fake.pyint(),
        choice(list(Weekday)),
        [meeting for meeting, _ in zip(fake_meeting(), range(6))],
    )
