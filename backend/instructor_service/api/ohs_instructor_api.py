import attr

from instructor_service.api.course_api import CourseApi


@attr.s(auto_attribs=True, slots=True)
class OhsInstructorApi:
    course_api: CourseApi
