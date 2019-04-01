import attr

from core.api.course_api import CourseApi
from core.api.instructor_api import InstructorApi
from core.api.meeting_api import MeetingApi
from core.api.student_api import StudentApi


@attr.s(auto_attribs=True, slots=True)
class OhsApi:
    course_api: CourseApi
    instructor_api: InstructorApi
    student_api: StudentApi
    meeting_api: MeetingApi
