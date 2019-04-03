import graphene

from core.domain.user import Instructor as DomainInstructor
from core.gql.context import meeting_api
from core.gql.schema.meeting_schema import Meeting
from core.gql.schema_registry import SchemaRestriction, register_query


@register_query(allow=SchemaRestriction.ALL)
class MeetingQuery(graphene.ObjectType):
    meeting = graphene.Field(Meeting, meeting_id=graphene.UUID(required=True))
    upcoming_meetings = graphene.List(Meeting)
    meetings = graphene.List(
        Meeting,
        office_hour_id=graphene.UUID(required=True),
        start_time=graphene.Int(required=True),
        end_time=graphene.Int(required=True),
    )

    def resolve_meeting(self, info, meeting_id):
        return (
            meeting_api(info).get_meeting(meeting_id).map_or(Meeting.from_domain, None)
        )

    def resolve_meetings(self, info, office_hour_id, start_time, end_time):
        return [
            Meeting.from_domain(meeting)
            for meeting in meeting_api(info).get_meetings_of_officehour_for_date(
                office_hour_id, start_time, end_time
            )
        ]

    def resolve_upcoming_meetings(self, info):
        user = info.context.user
        if isinstance(user, DomainInstructor):
            meetings = meeting_api(info).get_meetings_of_instructor(user.user_name)
        else:
            meetings = meeting_api(info).get_meetings_of_student(user.student_number)

        return [Meeting.from_domain(meeting) for meeting in meetings]
