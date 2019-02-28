import graphene

from common.domain.course import Semester


def semester_description(value):
    if value == Semester.FULL_YEAR:
        return "Full year long course"
    else:
        return f"The {value.name.lower()} semester"


Semester = graphene.Enum.from_enum(Semester, description=semester_description)


class Course(graphene.ObjectType):
    course_code = graphene.String()


class Session(graphene.ObjectType):
    year = graphene.Int()
    semester = graphene.Field(Semester)


class Section(graphene.ObjectType):
    course = Course
    session = Session
    section_code = graphene.String()
    num_students = graphene.Int()
