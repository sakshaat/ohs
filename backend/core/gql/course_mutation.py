import graphene

from core.domain.course import Semester as DomainSemester
from core.gql.context import course_api, instructor_api
from core.gql.course_schema import Course, CourseInput, Section, SectionInput
from core.gql.schema_registry import SchemaRestriction, register_mutation


@register_mutation(allow=SchemaRestriction.INSTRUCTOR)
class CreateCourse(graphene.Mutation):
    class Arguments:
        course_input = CourseInput(required=True)

    Output = Course

    def mutate(self, info, course_input):
        return course_api(info).create_course(course_input.course_code).unwrap()


@register_mutation(allow=SchemaRestriction.INSTRUCTOR)
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
            .expect(f"Instructor with username {taught_by} does not exist.")
            if taught_by
            else info.context.user
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
