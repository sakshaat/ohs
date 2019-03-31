from uuid import UUID

import attr

from core.domain.user import Instructor, Student, User


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
    time_stamp: int
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
    time_stamp: int
    content_text: str


@attr.s(slots=True, auto_attribs=True, frozen=True)
class Meeting:
    """
    Represents a booked meeting between Instructor and Student.

    Args:
        meeting_id: Unique UUID to identify meetings
        office_hour_id: ID of office hour the meeting belongs to
        index: Index of the meeting in the office hour
        instructor: Instructor
        student: Student
        notes: List of Notes of meeting
        comments: List of comments of meeting
        start_time: Start date/time of meeting
    """

    meeting_id: UUID
    officehour_id: UUID
    index: int
    instructor: Instructor
    student: Student
    notes: [Note]
    comments: [Comment]
    start_time: int
