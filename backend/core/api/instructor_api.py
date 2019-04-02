import attr
from option import Err, Ok, Option, Result

from core.authentication.password_auth import PasswordAuthenticator
from core.authentication.token_auth import JwtAuthenticator
from core.domain.user import Instructor
from core.persistence.instructor_persistence import InstructorPersistence


@attr.s(auto_attribs=True)
class InstructorApi:
    instructor_persistence: InstructorPersistence
    password_authenticator: PasswordAuthenticator
    jwt_authenticator: JwtAuthenticator

    def get_instructor(self, user_name: str) -> Option[Instructor]:
        return self.instructor_persistence.get_instructor(user_name)

    def create_instructor(
        self, first_name: str, last_name: str, user_name: str, password: str
    ) -> Result[Instructor, str]:
        password_hash = self.password_authenticator.crypto_context.hash(password)
        instructor = Instructor(first_name, last_name, user_name)
        return self.instructor_persistence.create_instructor(instructor, password_hash)

    def get_token(self, user_identity: str, password: str) -> Result[str, str]:
        authorized = self.password_authenticator.verify_password(
            user_identity, password
        )
        if authorized.is_err:
            return authorized
        return Ok(self.jwt_authenticator.generate_token(user_identity))

    def verify_instructor_by_token(self, token: str) -> Result[Instructor, str]:
        payload_result = self.jwt_authenticator.verify_token(token)
        if payload_result.is_err:
            return payload_result
        payload = payload_result.unwrap()
        user_name = payload.get("id")
        if not user_name:
            return Err("Invalid token")
        return self.get_instructor(user_name).map_or(
            Ok, (Err("UNAUTHORIZED - Could not get instructor"))
        )
