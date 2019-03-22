import attr

from core.domain.user import User, Instructor, Student
from uuid import UUID

@attr.s(slots=True, auto_attribs=True, frozen=True)
class Note:
    """
    Represents a note taken during a meeting.

    Args:
        note_id: Unique UUID to identify notes
        meeting_id: UUID of associated meeting
        time_stamp: date and time of creation
        content: content of note
    """

    note_id: UUID
    meeting_id: UUID
    time_stamp: str
    content_text: str


@attr.s(slots=True, auto_attribs=True, frozen=True)
class Comment:
    """
    Represents a comment on a meeting.

    Args:
        comment_id: Unique UUID to identify comment
        meeting_id: UUID of associated meeting
        author: User
        time_stamp: date and time of creation
        content: content of note
    """

    comment_id: UUID
    meeting_id: UUID
    author: User
    time_stamp: str
    content_text: str


@attr.s(slots=True, auto_attribs=True, frozen=True)
class Meeting:
    """
    Represents a booked meeting between Instructor and Student.

    Args:
        meeting_id: Unique UUID to identify meetings
        instructor: Instructor
        student: Student
        notes: List of Notes of meeting
        comments: List of comments of meeting
        start_time: Start date/time of meeting
        end_time: Duration of meeting
    """

    meeting_id: UUID
    instructor: Instructor
    student: Student
    notes: [Note]
    comments: [Comment]
    start_time: str
    end_time: str
