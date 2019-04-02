import graphene

from core.domain.course import Weekday
from core.gql.schema.course_schema import Section
from core.gql.schema.meeting_schema import Meeting


def weekday_description(value):
    if value:
        return value.name.capitalize()


Weekday = graphene.Enum.from_enum(Weekday, description=weekday_description)


class Slot(graphene.ObjectType):
    meeting = graphene.Field(Meeting, required=False)


class OfficeHour(graphene.ObjectType):
    officehour_id = graphene.UUID(required=True)
    section = graphene.Field(Section, required=True)
    starting_hour = graphene.Int(required=True)
    weekday = graphene.Field(Weekday, required=True)
    meetings = graphene.List(Slot, required=True)

    @classmethod
    def from_domain(cls, domain_office_hour):
        return cls(
            domain_office_hour.officehour_id,
            Section.from_domain(domain_office_hour.section),
            domain_office_hour.starting_hour,
            domain_office_hour.weekday,
            [
                Slot(Meeting.from_domain(meeting)) if meeting else Slot()
                for meeting in domain_office_hour.meetings
            ],
        )
