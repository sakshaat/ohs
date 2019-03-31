from typing import List

import attr
from option import Option, Result

from core.domain.course import Course, Section, SectionIdentity, Semester
from core.domain.user import Instructor
from core.persistence.course_persistence import CoursePersistence


@attr.s(auto_attribs=True)
class CourseApi:
    course_persistence: CoursePersistence

    def create_section(
        self,
        course: Course,
        year: int,
        semester: Semester,
        section_code: str,
        taught_by: Instructor,
        num_students: int = 0,
    ) -> Result[Section, str]:
        """
        Create a new section in the system.

        Args:
            course: The course that the section belongs to
            year: The year it is offered
            semester: semester of offering
            section_code: The section code for that section
            taught_by: The instructor for that section
            num_students: The number of students in that section

        Returns:
            The new section created
        """
        section = Section(course, year, semester, section_code, taught_by, num_students)
        return self.course_persistence.create_section(section)

    def create_course(self, course_code: str) -> Result[Course, str]:
        """
        Create a new course in the system.

        Args:
            course_code: The course code of the course

        Returns:
            The new course created
        """
        course = Course(course_code)
        return self.course_persistence.create_course(course)

    def query_courses(self, filters=None) -> List[Course]:
        """
        Query for courses is the system

        Args:
            filters: Filters to apply to the query

        Returns:
            List of courses returned by the query
        """
        return self.course_persistence.query_courses(filters)

    def query_sections(
        self, taught_by: str = None, enrolled_in: str = None, course_code: str = None
    ) -> List[Section]:
        """
        Query for sections is the system

        Args:
            taught_by: Filter by instroctor username of sections
            enrolled_in: Filter by student's student number enrolled in sections
            course_code: Filter by course code of sections

        Returns:
            List of sections returned by the query
        """

        filters = {
            "course_code": course_code,
            "taught_by": taught_by,
            "enrolled_in": enrolled_in,
        }
        
        # removing all None values, avoids having to check later
        filters = {k:v for k,v in filters.items() if v is not None}

        return self.course_persistence.query_sections(filters)

    def get_course(self, course_code: str) -> Option[Course]:
        """
        Get course by course code

        Args:
            course_code: The course code

        Returns:
            The course if found
        """
        return self.course_persistence.get_course(course_code)

    def get_section(self, section_identity: SectionIdentity) -> Option[Section]:
        """
        Get section by section code

        Args:
            section_identity: The identity of the section

        Returns:
            The section if found
        """
        return self.course_persistence.get_section(section_identity)
