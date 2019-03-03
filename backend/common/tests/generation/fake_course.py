from random import choice
import string

from common.domain.course import Course, Section, Semester
from common.tests.generation import fake

def id_generator(size=7, chars=string.ascii_uppercase + string.digits): 
    return ''.join(choice(chars) for _ in range(size))

def fake_course() -> Course:
    course_code = fake.pystr()
    return Course(course_code)

def fake_section(course=None, year=None, semester=None) -> Section:
    course = course or fake_course()
    year = year or choice(range(9999))
    semester = semester or choice(list(Semester))
    section_code = id_generator()
    num_students = fake.pyint()
    return Section(course, year, semester, num_students, section_code)
