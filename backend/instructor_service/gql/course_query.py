import graphene

from common.gql.course_schema import Course, Section
from instructor_service.api.course_api import CourseApi


def _course_api(info) -> CourseApi:
    return info.context.api.course_api


class CourseQuery(graphene.ObjectType):
    course = graphene.Field(Course, course_code=graphene.String(required=True))
    courses = graphene.List(
        Course, filters=graphene.String(required=False)
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
    section = graphene.Field(Section, section_code=graphene.String(required=True))
    sections = graphene.List(
        Section, filters=graphene.String(required=False)
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
