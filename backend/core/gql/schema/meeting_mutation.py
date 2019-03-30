import graphene

from core.gql.context import meeting_api
from core.gql.schema.meeting_schema import Comment, Note
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


@register_mutation(SchemaRestriction.ALL)
class CreateComment(graphene.Mutation):
    class Arguments:
        meeting_id = graphene.UUID(required=True)
        content_text = graphene.String(required=True)

    Output = Comment

    def mutate(self, info, meeting_id, content_text):
        return (
            meeting_api(info)
            .create_comment(meeting_id, info.context.user, content_text)
            .map(Comment.from_domain)
            .unwrap()
        )


@register_mutation(SchemaRestriction.INSTRUCTOR)
class CreateNote(graphene.Mutation):
    class Arguments:
        meeting_id = graphene.UUID(required=True)
        content_text = graphene.String(required=True)

    Output = Note

    def mutate(self, info, meeting_id, content_text):
        return (
            meeting_api(info)
            .create_note(meeting_id, info.context.user, content_text)
            .map(Note.from_domain)
            .unwrap()
        )
