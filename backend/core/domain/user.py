from abc import ABC

import attr


@attr.s(slots=True, frozen=True, auto_attribs=True)
class User(ABC):
    """
    An abstract user in the system
    """

    first_name: str
    last_name: str


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Instructor(User):
    """
    An instructor in the system
    """

    user_name: str


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Student(User):
    """
    A student in the system
    """

    student_number: str
