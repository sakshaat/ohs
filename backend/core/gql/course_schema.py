import graphene

from core.domain.course import (
    Course as DomainCourse,
    Section as DomainSection,
    SectionIdentity,
    Semester,
)
from core.gql.user_schema import Instructor


def semester_description(value):
    if value == Semester.FULL_YEAR:
        return "Full year long course"
    elif value:
        return f"The {value.name.lower()} semester"


Semester = graphene.Enum.from_enum(Semester, description=semester_description)


class Course(graphene.ObjectType):
    course_code = graphene.String(required=True)

    @classmethod
    def from_domain(cls, domain_course: DomainCourse):
        return cls(domain_course.course_code)

    def to_domain(self):
        return DomainCourse(self.course_code)


class Section(graphene.ObjectType):
    course = graphene.Field(Course, required=True)
    year = graphene.Int(required=True)
    semester = graphene.Field(Semester, required=True)
    section_code = graphene.String(required=True)
    taught_by = graphene.Field(Instructor, required=True)
    num_students = graphene.Int(required=True)

    @classmethod
    def from_domain(cls, domain_section: DomainSection):
        return cls(
            course=Course.from_domain(domain_section.course),
            year=domain_section.year,
            semester=domain_section.semester,
            section_code=domain_section.section_code,
            taught_by=Instructor.from_domain(domain_section.taught_by),
            num_students=domain_section.num_students,
        )

    def identity(self):
        return SectionIdentity(
            self.course.to_domain(), self.year, self.semester, self.section_code
        )
