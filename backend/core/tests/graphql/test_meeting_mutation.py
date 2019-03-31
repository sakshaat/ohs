from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from graphene.utils.str_converters import to_snake_case
from option import Err, Ok

from core.domain.user import Instructor
from core.tests.generation import fake
from core.tests.generation.fake_meeting import fake_comment, fake_meeting, fake_note
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


@pytest.mark.parametrize("success", [True, False])
def test_create_note(schema, success):
    note = next(fake_note())
    error = Err(fake.pystr())
    context = MagicMock()
    context.api.meeting_api.create_note.return_value = Ok(note) if success else error
    query = """
    mutation createNote($meetingId: UUID!, $contentText: String!) {
        createNote(meetingId: $meetingId, contentText: $contentText) {
            noteId
            meetingId
            timeStamp
            contentText
        }
    }
    """
    variables = {"meetingId": str(note.meeting_id), "contentText": note.content_text}
    result = schema.execute(query, context=context, variables=variables)
    if success:
        assert not result.errors
        for attr, val in result.data["createNote"].items():
            expected = getattr(note, to_snake_case(attr))
            if isinstance(expected, UUID):
                expected = str(expected)
            assert expected == val
    else:
        assert error.unwrap_err() in str(result.errors)
    context.api.meeting_api.create_note.assert_called_once_with(
        note.meeting_id, context.user, note.content_text
    )


@pytest.mark.parametrize("success", [True, False])
def test_delete_note(schema, success):
    context = MagicMock()
    note_id = uuid4()
    error = Err(fake.pystr())
    context.user = fake_instructor()
    context.api.meeting_api.delete_note.return_value = Ok(note_id) if success else error
    query = """
    mutation deleteNote($noteId: UUID!) {
        deleteNote(noteId: $noteId) {
            noteId
        }
    }
    """

    result = schema.execute(query, context=context, variables={"noteId": str(note_id)})
    if success:
        assert not result.errors
        assert result.data["deleteNote"] == {"noteId": str(note_id)}
    else:
        assert error.unwrap_err() in str(result.errors)
    context.api.meeting_api.delete_note.assert_called_once_with(note_id, context.user)


@pytest.mark.parametrize("success", [True, False])
def test_create_meeting(schema, success):
    context = MagicMock()
    meeting = next(fake_meeting())
    error = Err(fake.pystr())
    context.api.instructor_api.get_instructor.return_value = Ok(meeting.instructor)
    context.api.meeting_api.create_meeting.return_value = (
        Ok(meeting) if success else error
    )
    context.user = meeting.student
    query = """
    mutation createMeeting($instructor: String!, $officeHourId: UUID!, $index: Int!, $startTime:
    Int!) {
        createMeeting(instructor: $instructor, officeHourId: $officeHourId, index: $index,
        startTime: $startTime) {
            instructor {
                userName
            }
            student {
                studentNumber
            }
            officeHourId
            index
            startTime
            notes {
                noteId
            }
            comments {
                commentId
            }
        }
    }
    """
    result = schema.execute(
        query,
        context=context,
        variables={
            "instructor": meeting.instructor.user_name,
            "officeHourId": str(meeting.office_hour_id),
            "index": meeting.index,
            "startTime": meeting.start_time,
        },
    )
    if success:
        assert not result.errors
        create_meeting = result.data["createMeeting"]
        for attr in ("index", "startTime"):
            assert getattr(meeting, to_snake_case(attr)) == create_meeting[attr]
        assert str(meeting.office_hour_id) == create_meeting["officeHourId"]
        assert create_meeting["notes"] == []
        assert create_meeting["comments"] == []
        assert create_meeting["instructor"]["userName"] == meeting.instructor.user_name
        assert (
            create_meeting["student"]["studentNumber"] == meeting.student.student_number
        )
    else:
        assert error.unwrap_err() in str(result.errors)
    context.api.instructor_api.get_instructor.assert_called_once_with(
        meeting.instructor.user_name
    )
    context.api.meeting_api.create_meeting.assert_called_once_with(
        meeting.instructor,
        context.user,
        meeting.office_hour_id,
        meeting.index,
        meeting.start_time,
    )
