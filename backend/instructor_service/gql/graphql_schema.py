import graphene

from core.gql import graphql_schema
from instructor_service.gql.course_query import (
    CourseQuery,
    CreateCourse,
    CreateSection,
    SectionQuery,
)


class Query(graphql_schema.Query, CourseQuery, SectionQuery):
    pass


class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    create_section = CreateSection.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
