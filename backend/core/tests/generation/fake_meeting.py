import time
from typing import Iterator
from uuid import uuid4

from core.domain.meeting import Comment, Meeting, Note
from core.tests.generation import fake
from core.tests.generation.fake_user import fake_instructor, fake_student


def fake_meeting() -> Iterator[Meeting]:
    while True:
        start_time = fake.date_time()
        yield Meeting(
            meeting_id=uuid4(),
            office_hour_id=uuid4(),
            index=abs(fake.pyint()),
            instructor=fake_instructor(),
            student=fake_student(),
            notes=[],
            comments=[],
            start_time=int(start_time.timestamp()),
        )


def fake_note() -> Iterator[Note]:
    while True:
        yield Note(
            note_id=uuid4(),
            meeting_id=uuid4(),
            time_stamp=int(time.time()),
            content_text=fake.pystr(),
        )


def fake_comment(author=None) -> Iterator[Comment]:
    while True:
        _author = author or fake_instructor()
        yield Comment(
            comment_id=uuid4(),
            meeting_id=uuid4(),
            author=_author,
            time_stamp=int(time.time()),
            content_text=fake.pystr(),
        )
