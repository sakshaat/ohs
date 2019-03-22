import attr
from option import Err, Ok, Result
from passlib.context import CryptContext

from core.persistence.authentication_persistence import AuthenticationPersistence


@attr.s(slots=True, frozen=True, auto_attribs=True)
class PasswordAuthenticator:
    authentication_persistence: AuthenticationPersistence
    algorithm: str = "argon2"
    crypto_context: CryptContext = CryptContext(algorithm)

    def update_password(self, user_identity: str, password: str) -> Result[None, str]:
        new_hash = self.crypto_context.hash(password)
        return self.authentication_persistence.update_password_hash(
            user_identity, new_hash
        )

    def verify_password(self, user_identity: str, password: str) -> Result[None, str]:
        get_hash_result = self.authentication_persistence.get_password_hash(
            user_identity
        )
        if get_hash_result.is_err:
            return get_hash_result

        correct_hash = get_hash_result.unwrap()
        verified, new_hash = self.crypto_context.verify_and_update(
            password, correct_hash
        )
        if not verified:
            return Err(f"Incorrect password for user: {user_identity}")
        if new_hash:
            return self.authentication_persistence.update_password_hash(
                user_identity, new_hash
            )
        return Ok(None)
