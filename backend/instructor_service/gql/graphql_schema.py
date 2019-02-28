import graphene

from common.gql import graphql_schema
from instructor_service.gql.course_query import CourseQuery, SectionQuery


class Query(graphql_schema.Query, CourseQuery, SectionQuery):
    pass


schema = graphene.Schema(query=Query)
