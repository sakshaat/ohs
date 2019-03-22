from typing import Callable, List
import uuid

import attr
from option import Err, Ok, Option, Result, maybe

from core.domain.meeting import Note, Comment, Meeting
from core.domain.user import Student, Instructor


@attr.s
class MeetingPresistence:
    """
    Presistence layer implementation for meeting related things.
    """

    # create_note, delete_note, get_note, get_notes
    get_connection = attr.ib(type=Callable)

    @property
    def connection(self):
        return self.get_connection()

    def create_note(self, note: Note) -> Result[Note, str]:
        if self.get_note(note.node_id):
            return Err(f"Note {note} already exists")
        elif not self.get_meeting(note.meeting_id):
            return Err(f"Meeting {note.meeting_id} does not exist")
        else:
            new_uuid = str(uuid.uuid4())
            while self.get_note(new_uuid):
                new_uuid = str(uuid.uuid4())
            c = self.connection.cursor()
            term = (new_uuid, note.meeting_id, note.time_stamp, note.content_text)
            c.execute(
                "INSERT INTO notes(note_id, meeting_id, time_stamp, "
                "content_text) VALUES (%s, %s, %s, %s)",
                term,
            )
            self.connection.commit()
            note.note_id = new_uuid
            return Ok(note)

    def get_note(self, note_id: str) -> Option[Note]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM notes WHERE note_id=%s", (note_id))
        note = None
        res = c.fetchone()
        if res:
            note = Note(note_id, res[1], res[2], res[3])
        return maybe(note)

    def get_notes_of_meeting(self, meeting_id) -> List[Note]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM notes WHERE meeting_id=%s", (meeting_id))
        notes = c.fetchall()
        if len(notes) > 0:
            notes = map(lambda res: Note(res[0], res[1], res[2], res[3]), notes)
        return list(notes)

    def delete_note(self, note_id: str) -> Result[str, str]:
        if not self.get_note(note_id):
            return Err(f"Note {note_id} does not exist")
        c = self.connection.cursor()
        c.execute("DELETE FROM notes WHERE note_id=%s", (note_id))
        self.connection.commit()
        return Ok(note_id)

    def create_comment(self, comment: Comment) -> Result[Comment, str]:
        if self.get_comment(comment.comment_id):
            return Err(f"Comment {comment} already exists")
        elif not self.get_meeting(comment.meeting_id):
            return Err(f"Meeting {comment.meeting_id} does not exist")
        else:
            new_uuid = str(uuid.uuid4())
            while self.get_comment(new_uuid):
                new_uuid = str(uuid.uuid4())
            c = self.connection.cursor()
            if isinstance(comment.author, Instructor):
                term = (
                    new_uuid,
                    comment.meeting_id,
                    comment.author,
                    None,
                    comment.time_stamp,
                    comment.content_text,
                )
            else:
                term = (
                    new_uuid,
                    comment.meeting_id,
                    None,
                    comment.author,
                    comment.time_stamp,
                    comment.content_text,
                )
            c.execute(
                "INSERT INTO comments(note_id, meeting_id, author_if_instructor,"
                " author_if_student, time_stamp, content_text) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                term,
            )
            self.connection.commit()
            comment.comment_id = new_uuid
            return Ok(comment)

    def _res_to_comment(self, res):
        if res[2] is None:
            author = res[3]
        else:
            author = res[2]
        return Comment(res[0], res[1], author, res[4], res[5])

    def get_comment(self, comment_id: str) -> Option[Comment]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM comments WHERE comment_id=%s", (comment_id))
        comment = None
        res = c.fetchone()
        if res:
            comment = self._res_to_comment(res)
        return maybe(comment)

    def get_comments_of_meeting(self, meeting_id) -> List[Comment]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM comments WHERE meeting_id=%s", (meeting_id))
        comments = c.fetchall()
        if len(comments) > 0:
            comments = map(lambda x: self._res_to_comment(x), comments)
        return list(comments)

    def delete_comment(self, comment_id: str) -> Result[str, str]:
        if not self.get_comment(comment_id):
            return Err(f"Comment {comment_id} does not exist")
        c = self.connection.cursor()
        c.execute("DELETE FROM comments WHERE comment_id=%s", (comment_id))
        self.connection.commit()
        return Ok(comment_id)

    def create_meeting(self, meeting: Meeting) -> Result[Meeting, str]:
        if self.get_meeting(meeting.meeting_id):
            return Err(f"Meeting {meeting} already exists")
        else:
            new_uuid = str(uuid.uuid4())
            while self.get_meeting(new_uuid):
                new_uuid = str(uuid.uuid4())
            c = self.connection.cursor()
            term = (
                new_uuid,
                meeting.instructor.user_name,
                meeting.student.student_number,
                meeting.start_time,
                meeting.end_time,
            )
            c.execute(
                "INSERT INTO meetings(meeting_id, instructor, student,"
                " start_time, end_time) "
                "VALUES (%s, %s, %s, %s, %s)",
                term,
            )
            self.connection.commit()
            return Ok(meeting)

    def _res_to_meeting(self, res):
        c = self.connection.cursor()

        def get_inst(user_name):
            c.execute("SELECT * FROM instructors WHERE user_name=%s", (str(user_name),))
            res = c.fetchone()
            if res:
                return Instructor(res[0], res[1], res[3])
            return None

        def get_stud(student_number):
            c.execute(
                "SELECT * FROM students WHERE student_number=%s", (str(student_number),)
            )
            res = c.fetchone()
            if res:
                return Student(res[0], res[1], res[3])
            return None

        return Meeting(
            res[0],
            get_inst(res[1]),
            get_stud(res[2]),
            self.get_notes_of_meeting(res[0]),
            self.get_comments_of_meeting(res[0]),
            res[3],
            res[4],
        )

    def get_meeting(self, meeting_id) -> Option[Meeting]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM meetings WHERE meeting_id=%s", (meeting_id))
        meeting = None
        res = c.fetchone()
        if res:
            meeting = self._res_to_meeting(res)
        return maybe(meeting)

    def get_meetings_of_instructor(self, user_name) -> List[Meeting]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM meetings WHERE instructor=%s", (user_name))
        meetings = c.fetchall()
        if len(meetings) > 0:
            meetings = map(lambda x: self._res_to_meeting(x), meetings)
        return list(meetings)

    def delete_meeting(self, meeting_id: str) -> Result[str, str]:
        if not self.get_meeting(meeting_id):
            return Err(f"Meeting {meeting_id} does not exist")
        c = self.connection.cursor()
        c.execute("DELETE FROM meetings WHERE meeting_id=%s", (meeting_id))
        self.connection.commit()
        return Ok(meeting_id)
