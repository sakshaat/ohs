import graphene

from core.domain.course import SectionIdentity, Semester as DomainSemester
from core.gql.context import course_api
from core.gql.schema.course_schema import Course, CourseInput, Section, Semester
from core.gql.schema_registry import SchemaRestriction, register_query


@register_query(allow=SchemaRestriction.ALL)
class CourseQuery(graphene.ObjectType):
    course = graphene.Field(Course, course_code=graphene.String(required=True))
    courses = graphene.List(
        Course, filters=graphene.String()
    )  # TODO: Use an actual filter

    def resolve_course(self, info, course_code):
        return course_api(info).get_course(course_code).map_or(Course.from_domain, None)

    def resolve_courses(self, info, filters=None):
        return [
            Course.from_domain(course)
            for course in course_api(info).query_courses(filters)
        ]


@register_query(allow=SchemaRestriction.ALL)
class SectionQuery(graphene.ObjectType):
    section = graphene.Field(
        Section,
        course=CourseInput(required=True),
        year=graphene.Int(required=True),
        semester=graphene.Argument(Semester, required=True),
        section_code=graphene.String(required=True),
    )
    sections = graphene.List(
        Section,
        taught_by=graphene.String(),
        enrolled_in=graphene.String(),
        course_code=graphene.String(),
    )

    def resolve_section(self, info, course, year, semester, section_code):
        return (
            course_api(info)
            .get_section(
                SectionIdentity(
                    course.to_domain(), year, DomainSemester(semester), section_code
                )
            )
            .map_or(Section.from_domain, None)
        )

    def resolve_sections(
        self,
        info,
        taught_by: str = None,
        enrolled_in: str = None,
        course_code: str = None,
    ):
        return [
            Section.from_domain(section)
            for section in course_api(info).query_sections(
                taught_by=taught_by, enrolled_in=enrolled_in, course_code=course_code
            )
        ]
