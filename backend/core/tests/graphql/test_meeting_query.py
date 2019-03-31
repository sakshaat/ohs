from unittest.mock import MagicMock

import pytest
from option import Some

from core.domain.user import Instructor
from core.tests.generation.fake_meeting import fake_comment, fake_meeting
from core.tests.generation.fake_user import fake_instructor, fake_student


class TestMeetingQuery:
    meeting_fragment = """
    fragment meetingDetails on Meeting {
        meetingId
        officeHourId
        index
        instructor {
            userName
            firstName
            lastName
        }
        student {
            studentNumber
            firstName
            lastName
        }
        notes {
            noteId
            meetingId
            timeStamp
            contentText
        }
        comments {
            commentId
            meetingId
            author {
                ... on Instructor {
                    userName
                    firstName
                    lastName
                }
                ... on Student {
                    studentNumber
                    firstName
                    lastName
                }
            }
            timeStamp
            contentText
        }
        startTime
    }
    """
    query_one = (
        """
    query getMeeting($meetingId: UUID!) {
        meeting(meetingId: $meetingId) {
            ... meetingDetails
        }
    }
    """
        + meeting_fragment
    )

    query_upcoming = (
        """
    query getUpcoming {
        upcomingMeetings {
            ... meetingDetails
        }
    }
    """
        + meeting_fragment
    )

    def test_query_one(self, schema):
        meeting = next(fake_meeting())
        meeting.comments.append(next(fake_comment(fake_student())))
        meeting.comments.append(next(fake_comment(fake_instructor())))
        context = MagicMock()
        context.api.meeting_api.get_meeting.return_value = Some(meeting)
        result = schema.execute(
            self.query_one,
            context=context,
            variables={"meetingId": str(meeting.meeting_id)},
        )
        assert not result.errors
        context.api.meeting_api.get_meeting.assert_called_once_with(meeting.meeting_id)
        assert result.data["meeting"]["meetingId"] == str(meeting.meeting_id)

    @pytest.mark.parametrize("user", [fake_instructor(), fake_student()])
    @pytest.mark.parametrize("amount", [0, 10])
    def test_query_upcoming(self, schema, user, amount):
        meetings = [meeting for meeting, _ in zip(fake_meeting(), range(amount))]
        context = MagicMock()
        context.user = user
        if isinstance(user, Instructor):
            api_method = context.api.meeting_api.get_meetings_of_instructor
            user_id = user.user_name
        else:
            api_method = context.api.meeting_api.get_meetings_of_student
            user_id = user.student_number
        api_method.return_value = meetings
        result = schema.execute(self.query_upcoming, context=context)
        assert not result.errors
        for gql_result, meeting in zip(result.data["upcomingMeetings"], meetings):
            assert gql_result["meetingId"] == str(meeting.meeting_id)
        api_method.assert_called_once_with(user_id)
