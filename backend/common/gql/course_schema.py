import graphene

from common.domain.course import (
    Course as DomainCourse,
    Section as DomainSection,
    Semester,
    Session as DomainSession,
)


def semester_description(value):
    if value == Semester.FULL_YEAR:
        return "Full year long course"
    elif value:
        return f"The {value.name.lower()} semester"


Semester = graphene.Enum.from_enum(Semester, description=semester_description)


class Course(graphene.ObjectType):
    course_code = graphene.String()

    @classmethod
    def from_domain(cls, domain_course: DomainCourse):
        return cls(domain_course.course_code)


class Session(graphene.ObjectType):
    year = graphene.Int()
    semester = graphene.Field(Semester)

    @classmethod
    def from_domain(cls, domain_session: DomainSession):
        return cls(year=domain_session.year, semester=domain_session.semester)


class Section(graphene.ObjectType):
    course = graphene.Field(Course)
    session = graphene.Field(Session)
    section_code = graphene.String()
    num_students = graphene.Int()

    @classmethod
    def from_domain(cls, domain_section: DomainSection):
        return cls(
            course=Course.from_domain(domain_section.course),
            session=Session.from_domain(domain_section.session),
            section_code=domain_section.section_code,
            num_students=domain_section.num_students,
        )
