from typing import List
from uuid import UUID, uuid4

import attr
from option import Option, Result

from core.domain.course import (
    Course,
    OfficeHour,
    Section,
    SectionIdentity,
    Semester,
    Weekday,
)
from core.domain.user import Instructor
from core.persistence.course_persistence import CoursePersistence
from core.persistence.meeting_persistence import MeetingPersistence


@attr.s(auto_attribs=True)
class CourseApi:
    course_persistence: CoursePersistence
    meeting_persistence: MeetingPersistence

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
        if enrolled_in:
            result = self.course_persistence.get_sections_of_student(enrolled_in)
            return [
                section
                for section in result
                if (not taught_by or section.taught_by.user_name == taught_by)
                and (not course_code or section.course.course_code == course_code)
            ]

        filters = {"course_code": course_code, "taught_by": taught_by}
        # removing all None values, avoids having to check later
        filters = {k: v for k, v in filters.items() if v is not None}
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

    def get_sections_of_student(self, student_number: str) -> List[Section]:
        """
        Get sections that a student is enrolled in.

        Args:
            student_number: Student Number of student.

        Returns:
            List of Sections returned by the query
        """
        return self.course_persistence.get_sections_of_student(student_number)

    def create_officehour(
        self, section: Section, starting_hour: int, weekday: Weekday
    ) -> Result[OfficeHour, str]:
        """
        Create a new section in the system.

        Args:
            section: The section of which this OfficeHour belongs to.
            starting_hour: (0-23) hour at which OfficeHour begins.
            weekday: day of week of this OffceHour

        Returns:
            The new OfficeHour created
        """
        officehour = OfficeHour(uuid4(), section, starting_hour, weekday, [])
        return self.course_persistence.create_officehour(
            officehour, self.meeting_persistence
        )

    def get_officehours_for_instructor_on_weekday(
        self, user_name: str, weekday: Weekday
    ) -> List[OfficeHour]:
        """
        Get office hours for instructor by day of the week

        Args:
            user_name: The user_name of the Instructor.
            weekday: The day of the week.

        Returns:
            List of officehours for instructor on that day.
        """
        return self.course_persistence.get_officehour_for_instructor_by_day(
            user_name, weekday, MeetingPersistence
        )

    def delete_officehour(self, office_hour_id: UUID) -> Result[UUID, str]:
        """
        Deletes OfficeHour of <office_hour_id>.

        Returns:
            office_hour_id on success
        """
        return self.course_persistence.delete_officehour(office_hour_id)
