import graphene

from common.domain.course import Course as DomainCourse
from common.gql.course_schema import Course, Section, Semester
from instructor_service.api.course_api import CourseApi


def _course_api(info) -> CourseApi:
    return info.context.api.course_api

class CourseQuery(graphene.ObjectType):
    course = graphene.Field(Course, course_code=graphene.String(required=True))
    courses = graphene.List(
        Course, filters=graphene.String()
    )  # TODO: Use an actual filter

    def resolve_course(self, info, course_code):
        return (
            _course_api(info).get_course(course_code).map_or(Course.from_domain, None)
        )

    def resolve_courses(self, info, filters=None):
        return [
            Course.from_domain(course)
            for course in _course_api(info).query_courses(filters)
        ]

class SectionQuery(graphene.ObjectType):
    section = graphene.Field(Section, section_code=graphene.UUID(required=True))
    sections = graphene.List(
        Section, filters=graphene.String()
    )  # TODO: Use an actual filter

    def resolve_section(self, info, section_code):
        return (
            _course_api(info)
            .get_section(section_code)
            .map_or(Section.from_domain, None)
        )

    def resolve_sections(self, info, filters=None):
        return [
            Section.from_domain(section)
            for section in _course_api(info).query_sections(filters)
        ]

class CourseInput(graphene.InputObjectType):
    course_code = graphene.String(required=True)

    def to_domain(self):
        return DomainCourse(self.course_code)


class CreateCourse(graphene.Mutation):
    class Arguments:
        course_input = CourseInput(required=True)

    Output = Course

    def mutate(self, info, course_input):
        return _course_api(info).create_course(course_input.course_code).unwrap()


class SectionInput(graphene.InputObjectType):
    course = CourseInput(required=True)
    year = graphene.Int(required=True)
    semester = graphene.Field(Semester, required=True)
    section_code = graphene.String(required=True)
    num_students = graphene.Int()


class CreateSection(graphene.Mutation):
    class Arguments:
        section_input = SectionInput(required=True)

    Output = Section

    def mutate(self, info, section_input):
        num_students = section_input.num_students or 0
        return (
            _course_api(info)
            .create_section(
                section_input.course.to_domain(),
                section_input.year,
                section_input.semester,
                section_input.section_code,
                num_students
            )
            .unwrap()
        )
