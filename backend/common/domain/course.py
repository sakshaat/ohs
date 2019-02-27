from enum import Enum, auto

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


@attr.s(slots=True, auto_attribs=True, frozen=True)
class Session:
    """
    Represents a session in the university (e.g. winter 2019)

    Args:
        year: The year of the session
        semester: The semester of the session
    """

    year: int
    semester: Semester


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Section:
    """
    Represents an actual course offering section.

    Args:
        course: The course of the section
        session: The session the section is in
        section_code: The section code
        num_students: The number of students in the section
    """

    course: Course
    session: Session
    section_code: str
    num_students: int = 0
