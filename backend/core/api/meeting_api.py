from typing import List

import attr
from option import Result
import uuid

from core.domain.meeting import Note, Meeting, Comment
from core.domain.user import User, Student, Instructor
from core.persistence.meeting_persistence import MeetingPersistence


@attr.s(auto_attribs=True)
class MeetingApi:
    meeting_persistence: MeetingPersistence

    def create_meeting(
        self, instructor: Instructor, student: Student, start_time: str, end_time: str
    ) -> Result[Meeting, str]:
        """
        Create a new meeting in the system.

        Args:
            instructor: Relevent instructor
            student: Relevent student
            start_time: Start time of meeting
            end_time: End time of meeting

        Returns:
            The new meeting created
        """
        meeting = Meeting(
            uuid.uuid4(), instructor, student, [], [], start_time, end_time
        )
        return self.meeting_persistence.create_meeting(meeting)

    def create_note(
        self, meeting_id: uuid.UUID, time_stamp: str, content_text: str
    ) -> Result[Note, str]:
        """
        Create a new note for the meeting <meeting_id>.

        Returns:
            The new Note created
        """
        note = Note(uuid.uuid4(), meeting_id, time_stamp, content_text)
        return self.meeting_persistence.create_note(note)

    def create_comment(
        self, meeting_id: uuid.UUID, author: User, time_stamp: str, content_text: str
    ) -> Result[Comment, str]:
        """
        Create a new comment for the meeting <meeting_id>.

        Returns:
            The new Comment created
        """
        comment = Comment(uuid.uuid4(), meeting_id, author, time_stamp, content_text)
        return self.meeting_persistence.create_comment(comment)

    def delete_note(self, note_id: uuid.UUID) -> Result[str, str]:
        """
        Deletes note of <note_id>.

        Returns:
            note_id on success
        """
        return self.meeting_persistence.delete_note(note_id)

    def delete_comment(self, comment_id: uuid.UUID) -> Result[str, str]:
        """
        Deletes comment of <comment_id>.

        Returns:
            comment_id on success
        """
        return self.meeting_persistence.delete_comment(comment_id)

    def delete_meeting(self, meeting_id: uuid.UUID) -> Result[str, str]:
        """
        Deletes meeting of <meeting_id>.

        Returns:
            meeting_id on success
        """
        return self.meeting_persistence.delete_meeting(meeting_id)

    def get_notes_of_meeting(self, meeting_id: uuid.UUID) -> List[Note]:
        """
        Gets all notes of the meeting <meeting_id>.

        Returns:
            List of notes
        """
        return self.meeting_persistence.get_notes_of_meeting(meeting_id)

    def get_comments_of_meeting(self, meeting_id: uuid.UUID) -> List[Comment]:
        """
        Gets all comments of the meeting <meeting_id>.

        Returns:
            List of comments
        """
        return self.meeting_persistence.get_comments_of_meeting(meeting_id)

    def get_meetings_of_instructor(self, user_name: str) -> List[Meeting]:
        """
        Gets all meetings of the instructor <user_name>.

        Returns:
            List of meetings
        """
        return self.meeting_persistence.get_meetings_of_instructor(user_name)
