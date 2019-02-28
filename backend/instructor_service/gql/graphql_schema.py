import graphene

from common.gql import graphql_schema
from instructor_service.gql.course_query import CourseQuery


class Query(graphql_schema.Query, CourseQuery):
    pass


schema = graphene.Schema(query=Query)
