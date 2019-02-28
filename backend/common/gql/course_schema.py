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


class CourseQuery(graphene.ObjectType):
    course = graphene.Field(Course, course_code=graphene.String(required=True))
    courses = graphene.List(
        Course, filters=graphene.String(required=False)
    )  # TODO: Use an actual filter

    def resolve_course(self, info, course_code):
        pass

    def resolve_courses(self, info, filters=None):
        pass


class Session(graphene.ObjectType):
    year = graphene.Int()
    semester = graphene.Field(Semester)


class Section(graphene.ObjectType):
    course = Course
    session = Session
    section_code = graphene.String()
    num_students = graphene.Int()
