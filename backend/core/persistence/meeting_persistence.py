import uuid
from typing import Callable, List

import attr
import time
from option import Err, Ok, Option, Result, maybe

from core.domain.meeting import Comment, Meeting, Note
from core.domain.user import Instructor, Student


@attr.s
class MeetingPersistence:
    """
    Persistence layer implementation for meeting related things.
    """

    # create_note, delete_note, get_note, get_notes
    get_connection = attr.ib(type=Callable)

    @property
    def connection(self):
        return self.get_connection()

    def create_note(self, note: Note) -> Result[Note, str]:
        if self.get_note(note.note_id):
            return Err(f"Note {note} already exists")
        elif not self.get_meeting(note.meeting_id):
            return Err(f"Meeting {note.meeting_id} does not exist")
        else:
            c = self.connection.cursor()
            term = (
                str(note.note_id),
                str(note.meeting_id),
                note.time_stamp,
                note.content_text,
            )
            c.execute(
                "INSERT INTO notes(note_id, meeting_id, time_stamp, "
                "content_text) VALUES (%s, %s, %s, %s)",
                term,
            )
            self.connection.commit()
            return Ok(note)

    def get_note(self, note_id: uuid.UUID) -> Option[Note]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM notes WHERE note_id=%s", (str(note_id)))
        note = None
        res = c.fetchone()
        if res:
            note = Note(note_id, uuid.UUID(res[1]), res[2], res[3])
        return maybe(note)

    def get_notes_of_meeting(self, meeting_id: uuid.UUID) -> List[Note]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM notes WHERE meeting_id=%s", (str(meeting_id)))
        notes = c.fetchall()
        if len(notes) > 0:
            notes = map(
                lambda res: Note(uuid.UUID(res[0]), uuid.UUID(res[1]), res[2], res[3]),
                notes,
            )
        return list(notes)

    def delete_note(self, note_id: uuid.UUID) -> Result[uuid.UUID, str]:
        if not self.get_note(note_id):
            return Err(f"Note {note_id} does not exist")
        c = self.connection.cursor()
        c.execute("DELETE FROM notes WHERE note_id=%s", (str(note_id)))
        self.connection.commit()
        return Ok(note_id)

    def create_comment(self, comment: Comment) -> Result[Comment, str]:
        if self.get_comment(comment.comment_id):
            return Err(f"Comment {comment} already exists")
        elif not self.get_meeting(comment.meeting_id):
            return Err(f"Meeting {comment.meeting_id} does not exist")
        else:
            c = self.connection.cursor()
            if isinstance(comment.author, Instructor):
                term = (
                    str(comment.comment_id),
                    str(comment.meeting_id),
                    comment.author,
                    None,
                    comment.time_stamp,
                    comment.content_text,
                )
            else:
                term = (
                    str(comment.comment_id),
                    str(comment.meeting_id),
                    None,
                    comment.author,
                    comment.time_stamp,
                    comment.content_text,
                )
            c.execute(
                "INSERT INTO comments(comment_id, meeting_id, author_if_instructor,"
                " author_if_student, time_stamp, content_text) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                term,
            )
            self.connection.commit()
            return Ok(comment)

    def _res_to_comment(self, res):
        c = self.connection.cursor()
        if res[2] is None:

            def get_stud(student_number):
                c.execute(
                    "SELECT * FROM students WHERE student_number=%s",
                    (str(student_number),),
                )
                sres = c.fetchone()
                if sres:
                    return Instructor(sres[0], sres[1], sres[3])
                return None

            author = get_stud(res[3])
        else:

            def get_inst(user_name):
                c.execute(
                    "SELECT * FROM instructors WHERE user_name=%s", (str(user_name),)
                )
                ires = c.fetchone()
                if ires:
                    return Instructor(ires[0], ires[1], ires[3])
                return None

            author = get_inst(res[2])
        return Comment(uuid.UUID(res[0]), uuid.UUID(res[1]), author, res[4], res[5])

    def get_comment(self, comment_id: uuid.UUID) -> Option[Comment]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM comments WHERE comment_id=%s", (str(comment_id)))
        comment = None
        res = c.fetchone()
        if res:
            comment = self._res_to_comment(res)
        return maybe(comment)

    def get_comments_of_meeting(self, meeting_id: uuid.UUID) -> List[Comment]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM comments WHERE meeting_id=%s", (str(meeting_id)))
        comments = c.fetchall()
        if len(comments) > 0:
            comments = map(lambda x: self._res_to_comment(x), comments)
        return list(comments)

    def delete_comment(self, comment_id: uuid.UUID) -> Result[uuid.UUID, str]:
        if not self.get_comment(comment_id):
            return Err(f"Comment {comment_id} does not exist")
        c = self.connection.cursor()
        c.execute("DELETE FROM comments WHERE comment_id=%s", (str(comment_id)))
        self.connection.commit()
        return Ok(comment_id)

    def create_meeting(self, meeting: Meeting) -> Result[Meeting, str]:
        if self.get_meeting(meeting.meeting_id):
            return Err(f"Meeting {meeting} already exists")
        else:
            c = self.connection.cursor()
            term = (
                str(meeting.meeting_id),
                meeting.office_hour_id,
                meeting.index,
                meeting.instructor.user_name,
                meeting.student.student_number,
                meeting.start_time,
            )
            c.execute(
                "INSERT INTO meetings(meeting_id, office_hour_id, index, instructor, student,"
                " start_time) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
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
            uuid.UUID(res[0]),
            uuid.UUID(res[1]),
            int(res[2]),
            get_inst(res[3]),
            get_stud(res[4]),
            self.get_notes_of_meeting(uuid.UUID(res[0])),
            self.get_comments_of_meeting(uuid.UUID(res[0])),
            res[5],
        )

    def get_meeting(self, meeting_id: uuid.UUID) -> Option[Meeting]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM meetings WHERE meeting_id=%s", (str(meeting_id)))
        meeting = None
        res = c.fetchone()
        if res:
            meeting = self._res_to_meeting(res)
        return maybe(meeting)

    def get_meetings_of_instructor(self, user_name: str) -> List[Meeting]:
        c = self.connection.cursor()
        c.execute(
            "SELECT * FROM meetings WHERE instructor=%s AND start_time>=%s"
            " ORDER BY start_time ASC",
            (user_name, int(time.time())),
        )
        meetings = c.fetchall()
        if len(meetings) > 0:
            meetings = map(lambda x: self._res_to_meeting(x), meetings)
        return list(meetings)

    def get_meetings_of_student(self, student_number: str) -> List[Meeting]:
        c = self.connection.cursor()
        c.execute(
            "SELECT * FROM meetings WHERE student=%s AND start_time>=%s ORDER BY start_time ASC",
            (student_number, int(time.time())),
        )
        meetings = c.fetchall()
        if len(meetings) > 0:
            meetings = map(lambda x: self._res_to_meeting(x), meetings)
        return list(meetings)

    def get_meetings_of_officehour_for_date(
        self, office_hour_id: uuid.UUID, range_start: int, range_end: int
    ) -> List[Meeting]:
        c = self.connection.cursor()
        c.execute(
            "SELECT * FROM meetings WHERE office_hour_id=%s AND start_time>=%s AND start_time<=%s"
            " ORDER BY start_time ASC",
            (office_hour_id, range_start, range_end),
        )
        meetings = c.fetchall()
        if len(meetings) > 0:
            meetings = map(lambda x: self._res_to_meeting(x), meetings)
        return list(meetings)

    def delete_meeting(self, meeting_id: uuid.UUID) -> Result[uuid.UUID, str]:
        if not self.get_meeting(meeting_id):
            return Err(f"Meeting {meeting_id} does not exist")
        c = self.connection.cursor()
        c.execute("DELETE FROM meetings WHERE meeting_id=%s", (str(meeting_id)))
        self.connection.commit()
        return Ok(meeting_id)

    def get_meetings_of_officehour(self, office_hour_id: uuid.UUID) -> List[Meeting]:
        c = self.connection.cursor()
        c.execute(
            "SELECT * FROM meetings WHERE office_hour_id=%s", (str(office_hour_id))
        )
        meetings = c.fetchall()
        if len(meetings) > 0:
            meetings = map(lambda x: self._res_to_meeting(x), meetings)
        return list(meetings)
