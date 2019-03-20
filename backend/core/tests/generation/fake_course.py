from random import choice

from core.domain.course import Course, Section, Semester
from core.tests.generation import fake
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
