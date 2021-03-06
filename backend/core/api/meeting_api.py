import time
from typing import List
from uuid import UUID, uuid4

import attr
from option import Err, Ok, Option, Result

from core.domain.meeting import Comment, Meeting, Note
from core.domain.user import Instructor, Student, User
from core.persistence.meeting_persistence import MeetingPersistence


@attr.s(auto_attribs=True)
class MeetingApi:
    meeting_persistence: MeetingPersistence

    def create_meeting(
        self,
        instructor: Instructor,
        student: Student,
        office_hour_id: UUID,
        index: int,
        start_time: int,
    ) -> Result[Meeting, str]:
        """
        Create a new meeting in the system.

        Args:
            instructor: Relevent instructor
            student: Relevent student
            office_hour_id: ID of office hour the meeting belongs to
            index: Index of the meeting in the office hour
            start_time: Start time of meeting

        Returns:
            The new meeting created
        """
        meeting = Meeting(
            meeting_id=uuid4(),
            office_hour_id=office_hour_id,
            index=index,
            instructor=instructor,
            student=student,
            notes=[],
            comments=[],
            start_time=start_time,
        )
        return self.meeting_persistence.create_meeting(meeting)

    def create_note(
        self, meeting_id: UUID, author: Instructor, content_text: str
    ) -> Result[Note, str]:
        """
        Create a new note for the meeting <meeting_id>.

        Returns:
            The new Note created
        """
        check_user = self._check_meeting_user(
            meeting_id, author, "Cannot make a not on meetings that you don't belong to"
        )
        if not check_user:
            return check_user
        time_stamp = int(time.time())
        note = Note(uuid4(), meeting_id, time_stamp, content_text)
        return self.meeting_persistence.create_note(note)

    def create_comment(
        self, meeting_id: UUID, author: User, content_text: str
    ) -> Result[Comment, str]:
        """
        Create a new comment for the meeting <meeting_id>.

        Returns:
            The new Comment created
        """
        check_user = self._check_meeting_user(
            meeting_id, author, "Cannot comment on meetings which you don't belong to"
        )
        if not check_user:
            return check_user
        time_stamp = int(time.time())
        comment = Comment(uuid4(), meeting_id, author, time_stamp, content_text)
        return self.meeting_persistence.create_comment(comment)

    def delete_note(self, note_id: UUID, author: Instructor) -> Result[UUID, str]:
        """
        Deletes note of <note_id>.

        Returns:
            note_id on success
        """
        note_result = self.meeting_persistence.get_note(note_id)
        if not note_result:
            return Err(f"Note with ID: '{note_id}' does not exist")
        meeting_id = note_result.unwrap().meeting_id
        meeting_result = self.meeting_persistence.get_meeting(meeting_id)
        if not meeting_result:
            return Err(f"Meeting with ID: '{meeting_id}' does not exist")
        if author != meeting_result.unwrap().instructor:
            return Err("Cannot delete a note that does not belong to you")
        return self.meeting_persistence.delete_note(note_id)

    def delete_comment(self, comment_id: UUID) -> Result[UUID, str]:
        """
        Deletes comment of <comment_id>.

        Returns:
            comment_id on success
        """
        return self.meeting_persistence.delete_comment(comment_id)

    def delete_meeting(self, meeting_id: UUID, user: User) -> Result[UUID, str]:
        """
        Deletes meeting of <meeting_id>.

        Returns:
            meeting_id on success
        """
        check_user = self._check_meeting_user(
            meeting_id, user, "Cannot delete meeting that you are not a part of"
        )
        if not check_user:
            return check_user
        return self.meeting_persistence.delete_meeting(meeting_id)

    def get_meeting(self, meeting_id: UUID) -> Option[Meeting]:
        """
        Get meeting by ID

        Args:
            meeting_id: The meeting Id

        Returns:
            Meeting if found
        """
        return self.meeting_persistence.get_meeting(meeting_id)

    def get_meetings_of_instructor(self, user_name: str) -> List[Meeting]:
        """
        Gets all upcoming meetings of the instructor <user_name>.

        Returns:
            List of meetings
        """
        return self.meeting_persistence.get_meetings_of_instructor(user_name)

    def get_meetings_of_student(self, student_number: str) -> List[Meeting]:
        """
        Gets all upcoming meetings of the student <student_number>.

        Returns:
            List of meetings
        """
        return self.meeting_persistence.get_meetings_of_student(student_number)

    def _check_meeting_user(
        self, meeting_id: UUID, user: User, error_msg: str
    ) -> Result[None, str]:
        meeting_result = self.meeting_persistence.get_meeting(meeting_id)
        if not meeting_result:
            return Err(f"Meeting with ID: '{meeting_id}' does not exist")
        meeting = meeting_result.unwrap()
        if user not in (meeting.instructor, meeting.student):
            return Err(error_msg)
        return Ok(None)
