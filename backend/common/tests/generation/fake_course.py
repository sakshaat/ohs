from random import choice

from common.domain.course import Course, Section, Semester
from common.tests.generation import fake


def fake_course() -> Course:
    course_code = fake.pystr()
    return Course(course_code)


def fake_section(course=None, year=None, semester=None) -> Section:
    course = course or fake_course()
    year = year or int(fake.year())
    semester = semester or choice(list(Semester))
    section_code = fake.pystr()
    num_students = fake.pyint()
    return Section(course, year, semester, section_code, num_students)
