import graphene

from core.gql.context import instructor_api, meeting_api
from core.gql.schema.meeting_schema import Comment, Meeting, Note
from core.gql.schema_registry import SchemaRestriction, register_mutation


@register_mutation(SchemaRestriction.ALL)
class DeleteMeeting(graphene.Mutation):
    class Arguments:
        meeting_id = graphene.UUID(required=True)

    meeting_id = graphene.UUID(required=True)

    def mutate(self, info, meeting_id):
        user = info.context.user
        return (
            meeting_api(info)
            .delete_meeting(meeting_id, user)
            .map(DeleteMeeting)
            .unwrap()
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


@register_mutation(SchemaRestriction.INSTRUCTOR)
class DeleteNote(graphene.Mutation):
    class Arguments:
        note_id = graphene.UUID(required=True)

    note_id = graphene.UUID(required=True)

    def mutate(self, info, note_id):
        return (
            meeting_api(info)
            .delete_note(note_id, info.context.user)
            .map(DeleteNote)
            .unwrap()
        )


@register_mutation(SchemaRestriction.STUDENT)
class CreateMeeting(graphene.Mutation):
    class Arguments:
        instructor = graphene.String(required=True)
        office_hour_id = graphene.UUID(required=True)
        index = graphene.Int(required=True)
        start_time = graphene.Int(required=True)

    Output = Meeting

    def mutate(self, info, instructor, office_hour_id, index, start_time):
        student = info.context.user
        instructor = instructor_api(info).get_instructor(instructor).unwrap()
        return (
            meeting_api(info)
            .create_meeting(instructor, student, office_hour_id, index, start_time)
            .map(Meeting.from_domain)
            .unwrap()
        )
