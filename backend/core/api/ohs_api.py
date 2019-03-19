import attr

from core.api.course_api import CourseApi
from core.api.instructor_api import InstructorApi


@attr.s(auto_attribs=True, slots=True)
class OhsApi:
    course_api: CourseApi
    instructor_api: InstructorApi
