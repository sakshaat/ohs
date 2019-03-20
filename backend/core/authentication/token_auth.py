import attr
import jwt
from jwt import InvalidTokenError
from option import Err, Ok, Result


@attr.s(frozen=True, auto_attribs=True, slots=True)
class JwtAuthenticator:
    secret: str
    algorithm: str = "HS256"

    def generate_token(self, user_identity: str) -> str:
        """
        Generate a JWT for a given user identity

        Args:
            user_identity: The user identity

        Returns:
            A JWT with payload {"id": user_identity}
        """
        return jwt.encode(
            {"id": user_identity}, self.secret, algorithm=self.algorithm
        ).decode("utf8")

    def verify_token(self, token: str) -> Result[dict, str]:
        """
        Verify a JWT token

        Args:
            token: The jwt to verify

        Returns:
            The payload of the verified JWT
        """
        try:
            return Ok(jwt.decode(token, self.secret, algorithms=[self.algorithm]))
        except InvalidTokenError:
            return Err("Invalid JWT token")
