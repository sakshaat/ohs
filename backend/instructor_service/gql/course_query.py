import graphene

from common.gql.course_schema import Course
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
            _course_api(info)
            .get_course(course_code)
            .map_or(lambda c: Course(c.course_code), None)
        )

    def resolve_courses(self, info, filters=None):
        return _course_api(info).query_courses(filters)
