from random import choice
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from option import maybe

from core.domain.course import Weekday
from core.tests.generation import list_fakes
from core.tests.generation.fake_course import fake_officehour, fake_section


@pytest.mark.parametrize("expected", [fake_officehour(), None])
def test_get_officehour(schema, expected):
    context = MagicMock()
    context.api.course_api.get_officehour.return_value = maybe(expected)
    office_hour_id = expected.office_hour_id if expected else uuid4()
    query = """
    query getOfficeHour($officeHourId: UUID!) {
        officehour(officeHourId: $officeHourId) {
            officeHourId
        }
    }
    """
    result = schema.execute(
        query, context=context, variables={"officeHourId": str(office_hour_id)}
    )
    assert not result.errors
    if expected:
        assert result.data["officehour"] == {"officeHourId": str(office_hour_id)}
    else:
        assert result.data["officehour"] is None


@pytest.mark.parametrize("expected", [[], list_fakes(fake_officehour, 10)])
def test_officehour_listing(schema, expected):
    context = MagicMock()
    context.api.course_api.get_officehours_for_section_on_weekday.return_value = (
        expected
    )
    weekday = choice(list(Weekday))
    section = fake_section()
    query = """
    query getOfficeHours($sectionInput: SectionInput!, $weekday: Weekday!) {
        officehours(sectionInput: $sectionInput, weekday: $weekday) {
            officeHourId
        }
    }
    """
    result = schema.execute(
        query,
        context=context,
        variables={
            "sectionInput": {
                "course": {"courseCode": section.course.course_code},
                "year": section.year,
                "semester": section.semester.name,
                "sectionCode": section.section_code,
                "taughtBy": section.taught_by.user_name,
                "numStudents": section.num_students,
            },
            "weekday": weekday.name,
        },
    )
    assert not result.errors
    assert result.data["officehours"] == [
        {"officeHourId": str(officehour.office_hour_id)} for officehour in expected
    ]
    context.api.course_api.get_officehours_for_section_on_weekday.assert_called_once_with(
        section.identity, weekday
    )
