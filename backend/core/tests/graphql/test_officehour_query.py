from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from option import maybe

from core.tests.generation.fake_course import fake_officehour


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
