from enum import Enum, auto
from typing import NamedTuple
from uuid import UUID

import attr

from core.domain.user import Instructor


class Semester(Enum):
    WINTER = auto()
    FALL = auto()
    SUMMER = auto()
    FULL_YEAR = auto()


class Weekday(Enum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()


@attr.s(slots=True, auto_attribs=True, frozen=True)
class Course:
    """
    Represents a course offered by the university, without the
    session/section info.

    Args:
        course_code: The course code for the coures (e.g. CSC302)
    """

    course_code: str


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Section:
    """
    Represents an actual course offering section.

    Args:
        course: The course of the section
        year: year of offering
        semester: semester of offering
        section_code: The section code
        taught_by: The instructor for this section
        num_students: The number of students in the section
    """

    course: Course
    year: int
    semester: Semester
    section_code: str
    taught_by: Instructor
    num_students: int = 0

    @property
    def identity(self):
        return SectionIdentity.from_section(self)


class SectionIdentity(NamedTuple):
    """
    Uniquelly identifies a section
    """

    course: Course
    year: int
    semester: Semester
    section_code: str

    @classmethod
    def from_section(cls, section: Section):
        return cls(section.course, section.year, section.semester, section.section_code)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class OfficeHour:
    """
    Represents a single office hour block with 6 slots for meetings to be booked.

    Args:
        section: Section for which this Office hour is held
        starting_hour: 0-23, starting hour of block
        weekday: Weekday
        meetings: [Meeting]
    """

    officehour_id: UUID
    section: Section
    starting_hour: int
    weekday: Weekday
    meetings: [Meeting] = [None, None, None, None, None, None]
