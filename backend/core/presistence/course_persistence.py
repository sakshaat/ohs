from typing import Dict, List, Callable

import attr
from option import Err, Ok, Option, Result, maybe

from core.domain.course import Course, Section, SectionIdentity


@attr.s
class CoursePresistence:
    """
    Presistence layer implementation for course related things.

    Dummy implementation for now, using Python dicts as the database.

    # TODO: Use an actual DB
    """

    # table courses(code text)
    get_connection = attr.ib(type=Callable)
    section_db = attr.ib(factory=dict, type=Dict[tuple, Section])

    @property
    def connection(self):
        return self.get_connection()

    def create_course(self, course: Course) -> Result[Course, str]:
        if self.get_course(course.course_code):
            return Err(f"Course {course} already exists")
        c = self.connection.cursor()
        term = (course.course_code,)
        c.execute("INSERT INTO courses VALUES (%s)", term)
        self.connection.commit()
        return Ok(course)

    def create_section(self, section: Section) -> Result[Section, str]:
        if self.get_section(section.identity):
            return Err(f"Section {section} already exists")
        elif not self.get_course(section.course.course_code):
            return Err(f"Course {section.course} does not exist")
        else:
            self.section_db[section.identity] = section
            return Ok(section)

    def get_course(self, course_code: str) -> Option[Course]:
        c = self.connection.cursor()
        term = (course_code,)
        c.execute("SELECT * FROM courses WHERE course_code=%s", term)
        course = None
        res = c.fetchone()
        if res:
            course = Course(res[0])
        return maybe(course)

    def get_section(self, section_identity: SectionIdentity) -> Option[Section]:
        return maybe(self.section_db.get(section_identity))

    def query_courses(self, filters=None) -> List[Course]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM courses")
        courses = c.fetchall()
        if len(courses) > 0:
            courses = map(lambda x: Course(x[0]), courses)
        return list(courses)

    def query_sections(self, filters=None) -> List[Section]:
        return list(self.section_db.values())
