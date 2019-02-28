from typing import List

import attr
from option import Result

from common.domain.course import Course, Section, Session
from instructor_service.presistence.course_persistence import CoursePresistence


@attr.s(auto_attribs=True)
class CourseApi:
    course_presistence: CoursePresistence

    def create_section(
        self, course: Course, session: Session, section_code: str, num_students: int = 0
    ) -> Result[Section, str]:
        """
        Create a new section in the system.

        Args:
            course: The course that the section belongs to
            session: The session that the section is in
            section_code: The section code
            num_students: The number of students in that section

        Returns:
            The new section created
        """
        section = Section(course, session, section_code, num_students)
        return self.course_presistence.create_section(section)

    def create_course(self, course_code: str) -> Result[Course, str]:
        """
        Create a new course in the system.

        Args:
            course_code: The course code of the course

        Returns:
            The new course created
        """
        course = Course(course_code)
        return self.course_presistence.create_course(course)

    def query_courses(self, filters=None) -> List[Course]:
        """
        Query for courses is the system

        Args:
            filters: Filters to apply to the query

        Returns:
            List of courses returned by the query
        """
        return self.course_presistence.query_courses(filters)

    def query_sections(self, filters=None) -> List[Section]:
        """
        Query for sections is the system

        Args:
            filters: Filters to apply to the query

        Returns:
            List of sections returned by the query
        """
        return self.course_presistence.query_sections(filters)
