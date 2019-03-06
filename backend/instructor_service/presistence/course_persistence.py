from typing import Dict, List
import sqlite3

import attr
from option import Err, Ok, Option, Result, maybe
import os

from common.domain.course import Course, Section, SectionIdentity


@attr.s
class CoursePresistence:
    """
    Presistence layer implementation for course related things.

    Dummy implementation for now, using Python dicts as the database.

    # TODO: Use an actual DB
    """

    # table courses(code text)
    section_db = attr.ib(factory=dict, type=Dict[tuple, Section])

    def __init__(self, connection):
        self.conn = connection
    
    def connect(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(os.listdir())
        self.conn = sqlite3.connect("common/main.db")
    
    def close(self):
        self.conn.close()

    def create_course(self, course: Course) -> Result[Course, str]:
        if self.get_course(course.course_code):
            return Err(f"Course {course} already exists")
        c = self.conn.cursor()
        term = (course.course_code,)
        c.execute('INSERT INTO courses VALUES (?)', term)
        self.conn.commit()
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
        c = self.conn.cursor()
        term = (course_code, )
        c.execute('SELECT * FROM courses WHERE code=?', term)
        course = None
        res = c.fetchone()
        if res:
            course = Course(res[0])
        return maybe(course)

    def get_section(self, section_identity: SectionIdentity) -> Option[Section]:
        return maybe(self.section_db.get(section_identity))

    def query_courses(self, filters=None) -> List[Course]:
        c = self.conn.cursor()
        c.execute('SELECT * FROM courses')
        courses = c.fetchall()
        if len(courses) > 0:
            courses = map(lambda x: x[0], courses)
        return list(courses)

    def query_sections(self, filters=None) -> List[Section]:
        return list(self.section_db.values())
