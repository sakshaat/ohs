from abc import ABC, abstractmethod

import attr


@attr.s(slots=True, frozen=True, auto_attribs=True)
class User(ABC):
    """
    An abstract user in the system
    """

    first_name: str
    last_name: str

    @abstractmethod
    def as_dict(self):
        pass


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Instructor(User):
    """
    An instructor in the system
    """

    user_name: str

    def as_dict(self):
        return {
            "userName": self.user_name,
            "firstName": self.first_name,
            "lastName": self.last_name,
        }


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Student(User):
    """
    A student in the system
    """

    student_number: str

    def as_dict(self):
        return {
            "studentNumber": self.student_number,
            "firstName": self.first_name,
            "lastName": self.last_name,
        }
