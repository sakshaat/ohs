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
            c = self.connection.cursor()
            term = (
                section.course.course_code,
                section.year,
                section.semester.value,
                section.section_code,
                section.taught_by.user_name,
                section.num_students,
            )
            c.execute(
                "INSERT INTO sections(course, year, semester, section_code, taught_by, num_students) VALUES (%s, %s, %s, %s, %s, %s)",
                term,
            )

            self.connection.commit()
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
        c = self.connection.cursor()
        term = (
            section_identity.course.course_code,
            section_identity.year,
            str(section_identity.semester.value),
            section_identity.section_code,
        )
        c.execute(
            "SELECT * FROM sections WHERE course=%s AND year=%s AND semester=%s AND section_code=%s",
            term,
        )
        section = None
        res = c.fetchone()
        if res:
            # TODO: get actual instructor object
            section = Section(
                Course(res[0]), res[1], Semester(int(res[2])), res[3], None, res[5]
            )
        return maybe(section)

    def query_courses(self, filters=None) -> List[Course]:
        c = self.connection.cursor()
        # TODO: filters
        c.execute("SELECT * FROM courses")
        courses = c.fetchall()
        if len(courses) > 0:
            courses = map(lambda x: Course(x[0]), courses)
        return list(courses)

    def query_sections(self, filters=None) -> List[Section]:
        c = self.connection.cursor()
        # TODO: filters
        c.execute("SELECT * FROM sections")
        sections = c.fetchall()
        if len(sections) > 0:
            # TODO: get actual instructor object
            courses = map(
                lambda res: Section(
                    Course(res[0]), res[1], Semester(int(res[2])), res[3], None, res[5]
                ),
                sections,
            )
        return list(sections)
