import graphene

from core.gql.context import meeting_api
from core.gql.schema_registry import SchemaRestriction, register_mutation


@register_mutation(SchemaRestriction.ALL)
class DeleteMeeting(graphene.Mutation):
    class Arguments:
        meeting_id = graphene.UUID(required=True)

    meeting_id = graphene.UUID(required=True)

    def mutate(self, info, meeting_id):
        user = info.context.user
        return DeleteMeeting(
            meeting_api(info).delete_meeting(meeting_id, user).unwrap()
        )
