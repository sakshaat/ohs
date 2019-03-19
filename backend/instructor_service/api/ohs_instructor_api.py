import attr

from instructor_service.api.course_api import CourseApi
from instructor_service.api.instructor_api import InstructorApi


@attr.s(auto_attribs=True, slots=True)
class OhsInstructorApi:
    course_api: CourseApi
    instructor_api: InstructorApi
