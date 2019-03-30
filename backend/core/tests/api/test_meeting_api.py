from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from option import Err, NONE, Ok, Some

from core.api.meeting_api import MeetingApi
from core.persistence.meeting_persistence import MeetingPersistence
from core.tests.generation import fake
from core.tests.generation.fake_meeting import fake_comment, fake_meeting, fake_note
from core.tests.generation.fake_user import fake_instructor, fake_student


@pytest.fixture()
def meeting_api():
    return MeetingApi(MagicMock(MeetingPersistence))


@pytest.mark.parametrize("user_type", ["instructor", "student"])
def test_check_meeting_user(meeting_api, user_type):
    meeting = next(fake_meeting())
    user = meeting.instructor if user_type == "instructor" else meeting.student
    meeting_api.meeting_persistence.get_meeting.return_value = Some(meeting)
    assert meeting_api._check_meeting_user(meeting.meeting_id, user, "").is_ok
    meeting_api.meeting_persistence.get_meeting.assert_called_once_with(
        meeting.meeting_id
    )


@pytest.mark.parametrize("user", [fake_student(), fake_instructor()])
def test_check_meeting_user_not_permitted(meeting_api, user):
    meeting = next(fake_meeting())
    meeting_api.meeting_persistence.get_meeting.return_value = Some(meeting)
    error = fake.pystr()
    assert (
        meeting_api._check_meeting_user(meeting.meeting_id, user, error).unwrap_err()
        == error
    )
    meeting_api.meeting_persistence.get_meeting.assert_called_once_with(
        meeting.meeting_id
    )


@pytest.mark.parametrize("user", [fake_student(), fake_instructor()])
def test_check_meeting_user_not_found(meeting_api, user):
    id_ = uuid4()
    meeting_api.meeting_persistence.get_meeting.return_value = NONE
    error = fake.pystr()
    assert (
        "does not exist"
        in meeting_api._check_meeting_user(id_, user, error).unwrap_err()
    )
    meeting_api.meeting_persistence.get_meeting.assert_called_once_with(id_)


@pytest.mark.parametrize("success", [True, False])
def test_create_meeting(meeting_api, success):
    meeting = next(fake_meeting())
    error = Err(fake.pystr())

    def assert_called_correctly(_meeting):
        assert meeting.meeting_id != _meeting.meeting_id
        for attr in (
            "office_hour_id",
            "index",
            "instructor",
            "student",
            "notes",
            "comments",
            "start_time",
        ):
            assert getattr(meeting, attr) == getattr(_meeting, attr)
        return Ok(meeting) if success else error

    meeting_api.meeting_persistence.create_meeting.side_effect = assert_called_correctly
    result = meeting_api.create_meeting(
        meeting.instructor,
        meeting.student,
        meeting.office_hour_id,
        meeting.index,
        meeting.start_time,
    )
    if success:
        assert result.unwrap() == meeting
    else:
        assert result == error
    meeting_api.meeting_persistence.create_meeting.assert_called_once()


@pytest.mark.parametrize("success", [True, False])
def test_create_note(meeting_api, success):
    note = next(fake_note())
    error = Err(fake.pystr())
    meeting = next(fake_meeting())

    def assert_called_correctly(_note):
        assert abs(note.time_stamp - _note.time_stamp) < 10
        assert note.note_id != _note.note_id
        assert note.meeting_id == _note.meeting_id
        assert note.content_text == _note.content_text
        return Ok(note) if success else error

    meeting_api.meeting_persistence.create_note.side_effect = assert_called_correctly
    meeting_api._check_meeting_user = MagicMock(return_value=Ok(None))

    result = meeting_api.create_note(
        note.meeting_id, meeting.instructor, note.content_text
    )
    if success:
        assert result.unwrap() == note
    else:
        assert result == error
    meeting_api.meeting_persistence.create_note.assert_called_once()
    meeting_api._check_meeting_user.assert_called_once()


@pytest.mark.parametrize("success", [True, False])
def test_create_comment(meeting_api, success):
    comment = next(fake_comment())
    error = Err(fake.pystr())

    def assert_called_correctly(_comment):
        assert abs(comment.time_stamp - _comment.time_stamp) < 10
        assert comment.comment_id != _comment.comment_id
        for attr in ("meeting_id", "author", "content_text"):
            assert getattr(comment, attr) == getattr(_comment, attr)
        return Ok(comment) if success else error

    meeting_api.meeting_persistence.create_comment.side_effect = assert_called_correctly
    meeting_api._check_meeting_user = MagicMock(return_value=Ok(None))
    result = meeting_api.create_comment(
        comment.meeting_id, comment.author, comment.content_text
    )
    if success:
        assert result.unwrap() == comment
    else:
        assert result == error

    meeting_api.meeting_persistence.create_comment.assert_called_once()
    meeting_api._check_meeting_user.assert_called_once()


@pytest.mark.parametrize("success", [True, False])
@pytest.mark.parametrize("delete_type", ["note", "comment"])
def test_delete(meeting_api, delete_type, success):
    id_ = uuid4()
    error = Err(fake.pystr())

    delete_method = getattr(meeting_api, f"delete_{delete_type}")
    delete_persistence_method = getattr(
        meeting_api.meeting_persistence, f"delete_{delete_type}"
    )

    delete_persistence_method.return_value = Ok(id_) if success else error
    result = delete_method(id_)
    if success:
        assert result.unwrap() == id_
    else:
        assert result == error
    delete_persistence_method.assert_called_once_with(id_)


@pytest.mark.parametrize("success", [True, False])
@pytest.mark.parametrize("user_type", ["instructor", "student"])
def test_delete_meeting(meeting_api, success, user_type):
    meeting = next(fake_meeting())
    error = Err(fake.pystr())
    meeting_api.meeting_persistence.delete_meeting.return_value = (
        Ok(meeting.meeting_id) if success else error
    )
    meeting_api._check_meeting_user = MagicMock(return_value=Ok(None))
    user = meeting.instructor if user_type == "instructor" else meeting.student
    result = meeting_api.delete_meeting(meeting.meeting_id, user)
    if success:
        assert result.unwrap() == meeting.meeting_id
    else:
        assert result == error
    meeting_api._check_meeting_user.assert_called_once_with(
        meeting.meeting_id, user, "Cannot delete meeting that you are not a part of"
    )
    meeting_api.meeting_persistence.delete_meeting.assert_called_once_with(
        meeting.meeting_id
    )


@pytest.mark.parametrize("user", [fake_instructor(), fake_student()])
def test_delete_meeting_fail_user_check(meeting_api, user):
    meeting = next(fake_meeting())
    error = Err(fake.pystr())
    meeting_api._check_meeting_user = MagicMock(return_value=error)
    assert meeting_api.delete_meeting(meeting.meeting_id, user) == error
    meeting_api.meeting_persistence.delete_meeting.assert_not_called()
    meeting_api._check_meeting_user.assert_called_once_with(
        meeting.meeting_id, user, "Cannot delete meeting that you are not a part of"
    )


@pytest.mark.parametrize("expected", [Some(next(fake_meeting())), NONE])
def test_get_meeting(meeting_api, expected):
    meeting_id = expected.unwrap().meeting_id if expected else uuid4()
    meeting_api.meeting_persistence.get_meeting.return_value = expected
    assert meeting_api.get_meeting(meeting_id) == expected
    meeting_api.meeting_persistence.get_meeting.assert_called_once_with(meeting_id)
    meeting_api.meeting_persistence.delete_meeting.assert_not_called()


def test_get_meetings_of_instructor(meeting_api):
    user_name = fake.pystr()
    expected = [meeting for meeting, _ in zip(fake_meeting(), range(10))]
    meeting_api.meeting_persistence.get_meetings_of_instructor.return_value = expected
    assert meeting_api.get_meetings_of_instructor(user_name) == expected
    meeting_api.meeting_persistence.get_meetings_of_instructor.assert_called_once_with(
        user_name
    )


def test_get_meetings_of_student(meeting_api):
    student_number = fake.pystr()
    expected = [meeting for meeting, _ in zip(fake_meeting(), range(10))]
    meeting_api.meeting_persistence.get_meetings_of_student.return_value = expected
    assert meeting_api.get_meetings_of_student(student_number) == expected
    meeting_api.meeting_persistence.get_meetings_of_student.assert_called_once_with(
        student_number
    )
