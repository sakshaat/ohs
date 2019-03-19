import graphene

from common.domain.course import (
    Course as DomainCourse,
    SectionIdentity,
    Semester as DomainSemester,
)
from common.gql.course_schema import Course, Section, Semester
from instructor_service.gql.context import course_api, instructor_api


class CourseInput(graphene.InputObjectType):
    course_code = graphene.String(required=True)

    def to_domain(self):
        return DomainCourse(self.course_code)


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


class SectionQuery(graphene.ObjectType):
    section = graphene.Field(
        Section,
        course=CourseInput(required=True),
        year=graphene.Int(required=True),
        semester=graphene.Argument(Semester, required=True),
        section_code=graphene.String(required=True),
    )
    sections = graphene.List(
        Section, filters=graphene.String()
    )  # TODO: Use an actual filter

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

    def resolve_sections(self, info, filters=None):
        return [
            Section.from_domain(section)
            for section in course_api(info).query_sections(filters)
        ]


class CreateCourse(graphene.Mutation):
    class Arguments:
        course_input = CourseInput(required=True)

    Output = Course

    def mutate(self, info, course_input):
        return course_api(info).create_course(course_input.course_code).unwrap()


class SectionInput(graphene.InputObjectType):
    course = CourseInput(required=True)
    year = graphene.Int(required=True)
    semester = graphene.Field(Semester, required=True)
    section_code = graphene.String(required=True)
    taught_by = graphene.UUID()
    num_students = graphene.Int()


class CreateSection(graphene.Mutation):
    class Arguments:
        section_input = SectionInput(required=True)

    Output = Section

    def mutate(self, info, section_input):
        num_students = section_input.num_students or 0
        taught_by = section_input.taught_by
        instructor = (
            instructor_api(info)
            .get_instructor(taught_by)
            .expect(f"Instructor with ID {taught_by} does not exist.")
            if taught_by
            else info.context.instructor
        )

        return (
            course_api(info)
            .create_section(
                section_input.course.to_domain(),
                section_input.year,
                DomainSemester(section_input.semester),
                section_input.section_code,
                instructor,
                num_students,
            )
            .unwrap()
        )
