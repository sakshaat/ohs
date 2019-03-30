import graphene

from core.domain.meeting import Instructor as DomainInstructor, Meeting as DomainMeeting
from core.gql.schema.user_schema import Instructor, Student, UserTypes


class Note(graphene.ObjectType):
    note_id = graphene.UUID(required=True)
    meeting_id = graphene.UUID(required=True)
    time_stamp = graphene.Int(required=True)
    content_text = graphene.String(required=True)

    @classmethod
    def from_domain(cls, domain_note):
        return cls(
            domain_note.note_id,
            domain_note.meeting_id,
            domain_note.time_stamp,
            domain_note.content_text,
        )


class Comment(graphene.ObjectType):
    comment_id = graphene.UUID(required=True)
    meeting_id = graphene.UUID(required=True)
    author = graphene.Field(UserTypes, required=True)
    time_stamp = graphene.Int(required=True)
    content_text = graphene.String(required=True)

    @classmethod
    def from_domain(cls, domain_note):
        domain_author = domain_note.author
        author = (
            Instructor.from_domain(domain_author)
            if isinstance(domain_author, DomainInstructor)
            else Student.from_domain(domain_author)
        )
        return cls(
            domain_note.comment_id,
            domain_note.meeting_id,
            author,
            domain_note.time_stamp,
            domain_note.content_text,
        )


class Meeting(graphene.ObjectType):
    meeting_id = graphene.UUID(required=True)
    office_hour_id = graphene.UUID(required=True)
    index = graphene.Int(required=True)
    instructor = graphene.Field(Instructor, required=True)
    student = graphene.Field(Student, required=True)
    notes = graphene.List(Note, required=True)
    comments = graphene.List(Comment, required=True)
    start_time = graphene.Int(required=True)

    @classmethod
    def from_domain(cls, domain_meeting: DomainMeeting):
        return cls(
            meeting_id=domain_meeting.meeting_id,
            office_hour_id=domain_meeting.office_hour_id,
            index=domain_meeting.index,
            instructor=Instructor.from_domain(domain_meeting.instructor),
            student=Student.from_domain(domain_meeting.student),
            notes=[Note.from_domain(note) for note in domain_meeting.notes],
            comments=[
                Comment.from_domain(comment) for comment in domain_meeting.comments
            ],
            start_time=domain_meeting.start_time,
        )
