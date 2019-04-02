import graphene

from core.domain.course import Weekday as DomainWeekday
from core.gql.context import course_api
from core.gql.schema.course_schema import SectionInput
from core.gql.schema.officehour_schema import OfficeHour, Weekday
from core.gql.schema_registry import SchemaRestriction, register_mutation


@register_mutation(allow=SchemaRestriction.INSTRUCTOR)
class CreateOfficeHour(graphene.Mutation):
    class Arguments:
        section_input = SectionInput(required=True)
        starting_hour = graphene.Int(required=True)
        weekday = graphene.Argument(Weekday, required=True)

    Output = OfficeHour

    def mutate(self, info, section_input, starting_hour, weekday):
        section = course_api(info).get_section(section_input.to_identity()).unwrap()
        return (
            course_api(info)
            .create_officehour(section, starting_hour, DomainWeekday(weekday))
            .map(OfficeHour.from_domain)
            .unwrap()
        )
