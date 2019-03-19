from option import Option

from common.domain.user import Instructor


class InstructorApi:
    def get_instructor(self, user_name: str) -> Option[Instructor]:
        pass
