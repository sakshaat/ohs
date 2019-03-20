import jwt
import pytest

from core.authentication.token_auth import JwtAuthenticator
from core.tests.generation import fake

SECRET = fake.pystr()


@pytest.fixture
def jwt_authenticator():
    return JwtAuthenticator(SECRET)


def test_generate(jwt_authenticator):
    user_id = fake.pystr()
    assert jwt.decode(
        jwt_authenticator.generate_token(user_id),
        SECRET,
        algorithms=[jwt_authenticator.algorithm],
    ) == {"id": user_id}


def test_verify(jwt_authenticator):
    user_id = fake.pystr()
    token = jwt.encode(
        {"id": user_id}, SECRET, algorithm=jwt_authenticator.algorithm
    ).decode("utf8")
    assert jwt_authenticator.verify_token(token).unwrap() == {"id": user_id}


def test_verify_bad_token(jwt_authenticator):
    user_id = fake.pystr()
    token = (
        jwt.encode(
            {"id": user_id}, SECRET, algorithm=jwt_authenticator.algorithm
        ).decode("utf8")
        + "f"
    )
    assert jwt_authenticator.verify_token(token).is_err


def test_verify_bad_secret(jwt_authenticator):
    user_id = fake.pystr()
    token = jwt.encode(
        {"id": user_id}, SECRET + SECRET, algorithm=jwt_authenticator.algorithm
    ).decode("utf8")
    assert jwt_authenticator.verify_token(token).is_err
