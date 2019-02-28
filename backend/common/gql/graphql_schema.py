import graphene

from common.gql.course_schema import CourseQuery


class Health(graphene.ObjectType):
    ok = graphene.Boolean(default_value=True)


class HealthQuery(graphene.ObjectType):
    health = graphene.Field(Health)

    def resolve_health(self, info):
        return Health()


class Query(HealthQuery, CourseQuery, graphene.ObjectType):
    pass
