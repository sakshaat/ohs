from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from graphene.utils.str_converters import to_snake_case
from option import Err, Ok

from core.domain.user import Instructor
from core.tests.generation import fake
from core.tests.generation.fake_meeting import fake_comment
from core.tests.generation.fake_user import fake_instructor, fake_student


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


@pytest.mark.parametrize("success", [True, False])
@pytest.mark.parametrize("author", [fake_instructor(), fake_student()])
def test_create_comment(schema, author, success):
    context = MagicMock()
    comment = next(fake_comment())
    error = Err(fake.pystr())
    query = """
    mutation createComment($meetingId: UUID!, $contentText: String!) {
        createComment(meetingId: $meetingId, contentText: $contentText) {
            commentId
            meetingId
            author {
                ... on Instructor {
                    userName
                }
                ... on Student {
                    studentNumber
                }
            }
            timeStamp
            contentText
        }
    }
    """
    context.api.meeting_api.create_comment.return_value = (
        Ok(comment) if success else error
    )
    variables = {
        "meetingId": str(comment.meeting_id),
        "contentText": comment.content_text,
    }
    result = schema.execute(query, context=context, variables=variables)
    if success:
        assert not result.errors
        for key, val in result.data["createComment"].items():
            if key == "author":
                if isinstance(comment.author, Instructor):
                    assert val["userName"] == comment.author.user_name
                else:
                    assert val["studentNumber"] == comment.author.student_number
            else:
                expected = getattr(comment, to_snake_case(key))
                if isinstance(expected, UUID):
                    expected = str(expected)
                assert expected == val
    else:
        assert result.errors
        assert error.unwrap_err() in str(result.errors)
    context.api.meeting_api.create_comment.assert_called_once_with(
        comment.meeting_id, context.user, comment.content_text
    )
