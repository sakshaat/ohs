from random import choice
from uuid import uuid4

from common.domain.course import Course, Section, Semester, Session
from common.tests.generation import fake


def fake_course() -> Course:
    course_code = fake.pystr()
    return Course(course_code)


def fake_session() -> Session:
    year = int(fake.year())
    semester = choice(list(Semester))
    return Session(year, semester)


def fake_section(course=None, session=None) -> Section:
    course = course or fake_course()
    session = session or fake_session()
    section_code = uuid4()
    num_students = fake.pyint()
    return Section(course, session, num_students, section_code)
