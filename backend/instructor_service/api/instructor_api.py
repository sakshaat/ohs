from uuid import UUID

from option import Option

from common.domain.user import Instructor


class InstructorApi:
    def get_instructor(self, instructor_id: UUID) -> Option[Instructor]:
        pass
