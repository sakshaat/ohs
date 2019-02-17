import graphene


class Health(graphene.ObjectType):
    ok = graphene.Boolean(default_value=True)


class Query(graphene.ObjectType):
    health = graphene.Field(Health)

    def resolve_health(self, info):
        return Health()
