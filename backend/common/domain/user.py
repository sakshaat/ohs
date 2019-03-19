from abc import ABC
from uuid import UUID

import attr


@attr.s(slots=True, frozen=True, auto_attribs=True)
class User(ABC):
    """
    An abstract user in the system
    """

    id: UUID
    first_name: str
    last_name: str
    password_hash: str


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Instructor(User):
    """
    An instructor in the system
    """


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Student(User):
    """
    A student in the system
    """

    student_number: str
