import graphene

from core.domain.course import Weekday as DomainWeekday
from core.gql.context import course_api
from core.gql.schema.course_schema import SectionInput
from core.gql.schema.officehour_schema import OfficeHour, Weekday
from core.gql.schema_registry import SchemaRestriction, register_query


@register_query(allow=SchemaRestriction.ALL)
class OfficeHourQuery(graphene.ObjectType):
    officehour = graphene.Field(OfficeHour, office_hour_id=graphene.UUID(required=True))
    officehours = graphene.List(
        OfficeHour,
        section_input=SectionInput(required=True),
        weekday=graphene.Argument(Weekday, required=True),
    )

    def resolve_officehour(self, info, office_hour_id):
        return course_api(info).get_officehour(office_hour_id).unwrap_or(None)

    def resolve_officehours(self, info, section_input, weekday):
        return [
            OfficeHour.from_domain(officehour)
            for officehour in course_api(info).get_officehours_for_section_on_weekday(
                section_input.to_identity(), DomainWeekday(weekday)
            )
        ]
