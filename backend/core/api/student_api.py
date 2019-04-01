import attr
from option import Err, Ok, Option, Result

from core.authentication.password_auth import PasswordAuthenticator
from core.authentication.token_auth import JwtAuthenticator
from core.domain.user import Student
from core.persistence.student_persistence import StudentPersistence


@attr.s(auto_attribs=True)
class StudentApi:
    student_persistence: StudentPersistence
    password_authenticator: PasswordAuthenticator
    jwt_authenticator: JwtAuthenticator

    def get_student(self, student_number: str) -> Option[Student]:
        return self.student_persistence.get_student(student_number)

    def create_student(
        self, first_name: str, last_name: str, student_number: str, password: str
    ) -> Result[Student, str]:
        password_hash = self.password_authenticator.crypto_context.hash(password)
        student = Student(first_name, last_name, student_number)
        return self.student_persistence.create_student(student, password_hash)

    def get_token(self, user_identity: str, password: str) -> Result[str, str]:
        authorized = self.password_authenticator.verify_password(
            user_identity, password
        )
        if authorized.is_err:
            return authorized
        return Ok(self.jwt_authenticator.generate_token(user_identity))

    def verify_student_by_token(self, token: str) -> Result[Student, str]:
        payload_result = self.jwt_authenticator.verify_token(token)
        if payload_result.is_err:
            return payload_result
        payload = payload_result.unwrap()
        student_number = payload.get("id")
        if not student_number:
            return Err("Invalid token")
        return self.get_student(student_number).map_or(
            Ok, (Err("Could not get student"))
        )
