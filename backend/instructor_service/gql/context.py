import attr

from instructor_service.api.ohs_instructor_api import OhsInstructorApi


@attr.s(auto_attribs=True, slots=True)
class InstructorContext:
    api: OhsInstructorApi
