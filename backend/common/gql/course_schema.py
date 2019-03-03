import graphene

from common.domain.course import (
    Course as DomainCourse,
    Section as DomainSection,
    Semester
)

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


class Section(graphene.ObjectType):
    course = graphene.Field(Course, required=True)
    year = graphene.Int(required=True)
    semester = graphene.Field(Semester, required=True)
    section_code = graphene.String(required=True)
    num_students = graphene.Int(required=True)

    @classmethod
    def from_domain(cls, domain_section: DomainSection):
        return cls(
            course=Course.from_domain(domain_section.course),
            year=domain_section.year,
            semester=domain_section.semester,
            section_code=domain_section.section_code,
            num_students=domain_section.num_students
        )
