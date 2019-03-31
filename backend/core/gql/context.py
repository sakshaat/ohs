from typing import Union

import attr

from core.api.course_api import CourseApi
from core.api.instructor_api import InstructorApi
from core.api.meeting_api import MeetingApi
from core.api.ohs_api import OhsApi
from core.domain.user import Instructor, Student


@attr.s(auto_attribs=True, slots=True)
class Context:
    api: OhsApi
    user: Union[Instructor, Student]


def course_api(info) -> CourseApi:
    return info.context.api.course_api


def instructor_api(info) -> InstructorApi:
    return info.context.api.instructor_api


def meeting_api(info) -> MeetingApi:
    return info.context.api.meeting_api
