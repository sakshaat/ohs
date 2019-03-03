from random import choice
from uuid import uuid4

from common.domain.course import Course, Section, Semester
from common.tests.generation import fake


def fake_course() -> Course:
    course_code = fake.pystr()
    return Course(course_code)



def fake_section(course=None, year=None, semester=None) -> Section:
    course = course or fake_course()
    year = year or choice(range(9999))
    semester = semester or choice(list(Semester))
    section_code = uuid4()
    num_students = fake.pyint()
    return Section(course, year, semester, num_students, section_code)
