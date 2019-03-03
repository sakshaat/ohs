from typing import List
from uuid import UUID, uuid4

import attr
from option import Option, Result

from common.domain.course import Course, Section, Semester
from instructor_service.presistence.course_persistence import CoursePresistence


@attr.s(auto_attribs=True)
class CourseApi:
    course_presistence: CoursePresistence

    def create_section(
        self,
        course: Course,
        year: int,
        semester: Semester,
        section_code: str,
        num_students: int = 0,
    ) -> Result[Section, str]:
        """
        Create a new section in the system.

        Args:
            course: The course that the section belongs to
            year: The year it is offered
            semester: semester of offering
            section_code: The section code for that section
            num_students: The number of students in that section
            
        Returns:
            The new section created
        """
        section = Section(course, year, semester, num_students, section_code)
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

    def get_course(self, course_code: str) -> Option[Course]:
        """
        Get course by course code

        Args:
            course_code: The course code

        Returns:
            The course if found
        """
        return self.course_presistence.get_course(course_code)

    def get_section(self, section_code: str) -> Option[Section]:
        """
        Get section by section code

        Args:
            section_code: The section code

        Returns:
            The section if found
        """
        return self.course_presistence.get_section(section_code)
