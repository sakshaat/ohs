import graphene

from common import graphql_schema


class Query(graphql_schema.Query):
    pass


schema = graphene.Schema(query=Query)
