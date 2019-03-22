from unittest.mock import MagicMock

import pytest
from option import Err, NONE, Ok, Some, maybe

from core.api.instructor_api import InstructorApi
from core.authentication.password_auth import PasswordAuthenticator
from core.authentication.token_auth import JwtAuthenticator
from core.persistence.instructor_persistence import InstructorPersistence
from core.tests.generation import fake
from core.tests.generation.fake_user import fake_instructor


@pytest.fixture()
def instructor_api():
    return InstructorApi(
        MagicMock(InstructorPersistence),
        MagicMock(PasswordAuthenticator),
        MagicMock(JwtAuthenticator),
    )


@pytest.mark.parametrize("expected_instructor", [None, fake_instructor()])
def test_get_instructor(instructor_api, expected_instructor):
    instructor_api.instructor_persistence.get_instructor = MagicMock(
        return_value=maybe(expected_instructor)
    )
    user_name = expected_instructor.user_name if expected_instructor else fake.pystr()
    assert instructor_api.get_instructor(user_name) == maybe(expected_instructor)
    instructor_api.instructor_persistence.get_instructor.called_once_with(user_name)


@pytest.mark.parametrize("success", [True, False])
def test_create_instructor(instructor_api, success):
    instructor = fake_instructor()
    password = fake.pystr()
    password_hash = fake.sha256()
    error = Err(fake.pystr())

    instructor_api.password_authenticator.crypto_context.hash = MagicMock(
        return_value=password_hash
    )
    instructor_api.instructor_persistence.create_instructor.return_value = (
        Ok(instructor) if success else error
    )

    result = instructor_api.create_instructor(
        instructor.first_name, instructor.last_name, instructor.user_name, password
    )
    if success:
        assert result == Ok(instructor)
    else:
        assert result == error

    instructor_api.password_authenticator.crypto_context.hash.assert_called_once_with(
        password
    )
    instructor_api.instructor_persistence.create_instructor.assert_called_once_with(
        instructor, password_hash
    )


@pytest.mark.parametrize("success", [True, False])
def test_get_token(instructor_api, success):
    error = Err(fake.pystr())
    password = fake.pystr()
    token = fake.sha256()
    user_name = fake.pystr()
    instructor_api.password_authenticator.verify_password.return_value = (
        Ok(None) if success else error
    )
    instructor_api.jwt_authenticator.generate_token.return_value = token

    result = instructor_api.get_token(user_name, password)
    if success:
        assert result == Ok(token)
        instructor_api.jwt_authenticator.generate_token.assert_called_once_with(
            user_name
        )
    else:
        assert result == error
        instructor_api.jwt_authenticator.generate_token.assert_not_called()
    instructor_api.password_authenticator.verify_password.assert_called_once_with(
        user_name, password
    )


@pytest.mark.parametrize("instructor_found", [True, False])
def test_verify_token(instructor_api, instructor_found):
    token = fake.sha256()
    instructor = fake_instructor()
    instructor_api.jwt_authenticator.verify_token.return_value = Ok(
        {"id": instructor.user_name}
    )
    if instructor_found:
        instructor_api.get_instructor = MagicMock(return_value=Some(instructor))
        assert instructor_api.verify_instructor_by_token(token) == Ok(instructor)
    else:
        instructor_api.get_instructor = MagicMock(return_value=NONE)
        assert instructor_api.verify_instructor_by_token(token) == Err(
            "Could not get instructor"
        )
    instructor_api.jwt_authenticator.verify_token.assert_called_once_with(token)
    instructor_api.get_instructor.assert_called_once_with(instructor.user_name)


@pytest.mark.parametrize("token_decode_result", [Ok({}), Err(fake.pystr())])
def test_verify_token_fail(instructor_api, token_decode_result):
    token = fake.sha256()
    instructor_api.get_instructor = MagicMock()
    instructor_api.jwt_authenticator.verify_token.return_value = token_decode_result
    result = instructor_api.verify_instructor_by_token(token)
    if token_decode_result.is_err:
        assert result == token_decode_result
    else:
        assert result == Err("Invalid token")
    instructor_api.jwt_authenticator.verify_token.assert_called_once_with(token)
    instructor_api.get_instructor.assert_not_called()
