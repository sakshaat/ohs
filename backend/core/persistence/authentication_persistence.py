from abc import ABC, abstractmethod

from option import Result


class AuthenticationPersistence(ABC):
    @abstractmethod
    def get_password_hash(self, user_identity: str) -> Result[str, str]:
        pass

    @abstractmethod
    def update_password_hash(
        self, user_identity: str, new_hash: str
    ) -> Result[None, str]:
        pass
