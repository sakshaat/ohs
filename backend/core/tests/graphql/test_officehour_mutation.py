from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from option import Err, Ok, Some

from core.tests.generation import fake
from core.tests.generation.fake_course import fake_officehour


@pytest.mark.parametrize("success", [True, False])
def test_create_officehour(schema, success):
    context = MagicMock()
    officehour = fake_officehour()
    error = Err(fake.pystr())
    context.api.course_api.get_section.return_value = Some(officehour.section)
    context.api.course_api.create_officehour.return_value = (
        Ok(officehour) if success else error
    )
    query = """
    mutation createOfficeHour(
        $sectionInput: SectionInput!, $startingHour: Int!, $weekday: Weekday!
    ) {
        createOfficeHour(
            sectionInput: $sectionInput, startingHour: $startingHour, weekday: $weekday
        ) {
            officehourId
            section {
                sectionCode
            }
            startingHour
            weekday
            meetings {
                meeting {
                    meetingId
                }
            }
        }
    }
    """
    variables = {
        "sectionInput": {
            "course": {"courseCode": officehour.section.course.course_code},
            "year": officehour.section.year,
            "semester": officehour.section.semester.name,
            "sectionCode": officehour.section.section_code,
            "taughtBy": officehour.section.taught_by.user_name,
            "numStudents": officehour.section.num_students,
        },
        "startingHour": officehour.starting_hour,
        "weekday": officehour.weekday.name,
    }
    result = schema.execute(query, context=context, variables=variables)
    if success:
        assert not result.errors
        create_officehour = result.data["createOfficeHour"]
        assert create_officehour["officehourId"] == str(officehour.officehour_id)
        assert (
            create_officehour["section"]["sectionCode"]
            == officehour.section.section_code
        )
        assert create_officehour["weekday"] == officehour.weekday.name
        assert create_officehour["startingHour"] == officehour.starting_hour
        for slot, meeting in zip(create_officehour["meetings"], officehour.meetings):
            if not slot["meeting"]:
                assert not meeting
            else:
                assert slot["meeting"]["meetingId"] == str(meeting.meeting_id)
    else:
        assert error.unwrap_err() in str(result.errors)
    context.api.course_api.create_officehour.assert_called_once_with(
        officehour.section, officehour.starting_hour, officehour.weekday
    )


@pytest.mark.parametrize("success", [True, False])
def test_delete_office_hour(schema, success):
    context = MagicMock()
    officehour_id = uuid4()
    error = Err(fake.pystr())
    context.api.course_api.delete_officehour.return_value = (
        Ok(officehour_id) if success else error
    )
    query = """
    mutation deleteOfficeHour($id: UUID!) {
        deleteOfficeHour(officehourId: $id) {
            officehourId
        }
    }
    """
    result = schema.execute(
        query, context=context, variables={"id": str(officehour_id)}
    )
    if success:
        assert not result.errors
        assert result.data["deleteOfficeHour"]["officehourId"] == str(officehour_id)
    else:
        assert error.unwrap_err() in str(result.errors)
    context.api.course_api.delete_officehour.assert_called_once_with(officehour_id)
