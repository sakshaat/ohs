from typing import Dict

import attr
from option import Err, Ok, Option, Result, maybe

from common.domain.course import Course, Section


@attr.s
class CoursePresistence:
    """
    Presistence layer implementation for course related things.

    Dummy implementation for now, using Python dicts as the database.

    # TODO: Use an actual DB
    """

    course_db = attr.ib(factory=dict, type=Dict[str, Course])
    section_db = attr.ib(factory=dict, type=Dict[str, Section])

    def create_course(self, course: Course) -> Result[Course, str]:
        if self.get_course(course.course_code):
            return Err(f"Course {course} already exists")
        self.course_db[course.course_code] = course
        return Ok(course)

    def create_section(self, section: Section) -> Result[Section, str]:
        if self.get_section(section.section_code):
            return Err(f"Section {section} already exists")
        elif not self.get_course(section.course.course_code):
            return Err(f"Course {section.course} does not exist")
        else:
            self.section_db[section.section_code] = section
            return Ok(section)

    def get_course(self, course_code: str) -> Option[Course]:
        return maybe(self.course_db.get(course_code))

    def get_section(self, section_code: str) -> Option[Section]:
        return maybe(self.section_db.get(section_code))
