import attr

from common.domain.user import Instructor
from instructor_service.api.course_api import CourseApi
from instructor_service.api.instructor_api import InstructorApi
from instructor_service.api.ohs_instructor_api import OhsInstructorApi


@attr.s(auto_attribs=True, slots=True)
class InstructorContext:
    api: OhsInstructorApi
    instructor: Instructor


def course_api(info) -> CourseApi:
    return info.context.api.course_api


def instructor_api(info) -> InstructorApi:
    return info.context.api.instructor_api
