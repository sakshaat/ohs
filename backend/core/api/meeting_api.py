import time
import uuid
from typing import List

import attr
from option import Result

from core.domain.meeting import Comment, Meeting, Note
from core.domain.user import Instructor, Student, User
from core.persistence.meeting_persistence import MeetingPersistence


@attr.s(auto_attribs=True)
class MeetingApi:
    meeting_persistence: MeetingPersistence

    def create_meeting(
        self, instructor: Instructor, student: Student, start_time: int, end_time: int
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
        self, meeting_id: uuid.UUID, content_text: str
    ) -> Result[Note, str]:
        """
        Create a new note for the meeting <meeting_id>.

        Returns:
            The new Note created
        """
        time_stamp = int(time.time())
        note = Note(uuid.uuid4(), meeting_id, time_stamp, content_text)
        return self.meeting_persistence.create_note(note)

    def create_comment(
        self, meeting_id: uuid.UUID, author: User, content_text: str
    ) -> Result[Comment, str]:
        """
        Create a new comment for the meeting <meeting_id>.

        Returns:
            The new Comment created
        """
        time_stamp = int(time.time())
        comment = Comment(uuid.uuid4(), meeting_id, author, time_stamp, content_text)
        return self.meeting_persistence.create_comment(comment)

    def delete_note(self, note_id: uuid.UUID) -> Result[uuid.UUID, str]:
        """
        Deletes note of <note_id>.

        Returns:
            note_id on success
        """
        return self.meeting_persistence.delete_note(note_id)

    def delete_comment(self, comment_id: uuid.UUID) -> Result[uuid.UUID, str]:
        """
        Deletes comment of <comment_id>.

        Returns:
            comment_id on success
        """
        return self.meeting_persistence.delete_comment(comment_id)

    def delete_meeting(self, meeting_id: uuid.UUID) -> Result[uuid.UUID, str]:
        """
        Deletes meeting of <meeting_id>.

        Returns:
            meeting_id on success
        """
        return self.meeting_persistence.delete_meeting(meeting_id)

    def get_meetings_of_instructor(self, user_name: str) -> List[Meeting]:
        """
        Gets all meetings of the instructor <user_name>.

        Returns:
            List of meetings
        """
        return self.meeting_persistence.get_meetings_of_instructor(user_name)
