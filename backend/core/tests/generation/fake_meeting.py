import time
from typing import Iterator
from uuid import uuid4

from core.domain.meeting import Comment, Meeting, Note
from core.tests.generation import fake
from core.tests.generation.fake_user import fake_instructor, fake_student


def fake_meeting() -> Iterator[Meeting]:
    while True:
        start_time = fake.date_time()
        end_time = start_time + fake.time_delta()
        assert end_time > start_time
        yield Meeting(
            meeting_id=uuid4(),
            instructor=fake_instructor(),
            student=fake_student(),
            notes=[],
            comments=[],
            start_time=int(start_time.timestamp()),
            end_time=int(end_time.timestamp()),
        )


def fake_note() -> Iterator[Note]:
    while True:
        yield Note(
            note_id=uuid4(),
            meeting_id=uuid4(),
            time_stamp=int(time.time()),
            content_text=fake.pystr(),
        )


def fake_comment() -> Iterator[Comment]:
    while True:
        yield Comment(
            comment_id=uuid4(),
            meeting_id=uuid4(),
            author=fake_instructor(),
            time_stamp=int(time.time()),
            content_text=fake.pystr(),
        )
