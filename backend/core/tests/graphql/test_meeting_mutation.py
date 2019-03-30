from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from option import Err, Ok

from core.tests.generation import fake


@pytest.mark.parametrize("success", [True, False])
def test_delete_meeting(schema, success):
    context = MagicMock()
    error = Err(fake.pystr())
    meeting_id = uuid4()
    query = """
    mutation deleteMeeting($meetingId: UUID!) {
        deleteMeeting(meetingId: $meetingId) {
            meetingId
        }
    }
    """
    context.api.meeting_api.delete_meeting.return_value = (
        Ok(meeting_id) if success else error
    )
    variables = {"meetingId": str(meeting_id)}
    result = schema.execute(query, context=context, variables=variables)
    if success:
        assert not result.errors
        assert result.data["deleteMeeting"] == variables
    else:
        assert result.errors
