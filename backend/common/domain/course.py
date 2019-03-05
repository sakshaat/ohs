from enum import Enum, auto
from typing import NamedTuple

import attr


class Semester(Enum):
    WINTER = auto()
    FALL = auto()
    SUMMER = auto()
    FULL_YEAR = auto()


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
        num_students: The number of students in the section
    """

    course: Course
    year: int
    semester: Semester
    section_code: str
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
