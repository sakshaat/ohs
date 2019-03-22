from unittest.mock import MagicMock

import pytest
from option import Err, Ok
from passlib.context import CryptContext

from core.authentication.password_auth import PasswordAuthenticator
from core.persistence.authentication_persistence import AuthenticationPersistence
from core.tests.generation import fake


@pytest.fixture()
def password_authenticator():
    return PasswordAuthenticator(
        MagicMock(AuthenticationPersistence), "", MagicMock(CryptContext)
    )


def test_update_password(password_authenticator):
    user_id, password = fake.pystr(), fake.pystr()
    expected_hash = fake.sha256()
    password_authenticator.authentication_persistence.update_password_hash = MagicMock(
        return_value=Ok(None)
    )
    password_authenticator.crypto_context.hash = MagicMock(return_value=expected_hash)
    assert password_authenticator.update_password(user_id, password).unwrap() is None
    password_authenticator.crypto_context.hash.assert_called_once_with(password)
    password_authenticator.authentication_persistence.update_password_hash.assert_called_once_with(
        user_id, expected_hash
    )


def test_update_password_fail(password_authenticator):
    user_id, password = fake.pystr(), fake.pystr()
    expected_hash = fake.sha256()
    error = Err(fake.pystr())
    password_authenticator.authentication_persistence.update_password_hash = MagicMock(
        return_value=error
    )
    password_authenticator.crypto_context.hash = MagicMock(return_value=expected_hash)
    assert password_authenticator.update_password(user_id, password) == error
    password_authenticator.crypto_context.hash.assert_called_once_with(password)
    password_authenticator.authentication_persistence.update_password_hash.assert_called_once_with(
        user_id, expected_hash
    )


def test_verify_password_success(password_authenticator):
    user_id, password = fake.pystr(), fake.pystr()
    expected_hash = fake.sha256()
    password_authenticator.authentication_persistence.get_password_hash = MagicMock(
        return_value=Ok(expected_hash)
    )
    password_authenticator.authentication_persistence.update_password_hash = MagicMock()
    password_authenticator.crypto_context.verify_and_update = MagicMock(
        return_value=(True, None)
    )
    assert password_authenticator.verify_password(user_id, password).unwrap() is None
    password_authenticator.authentication_persistence.get_password_hash.assert_called_once_with(
        user_id
    )
    password_authenticator.authentication_persistence.update_password_hash.assert_not_called()
    password_authenticator.crypto_context.verify_and_update.assert_called_once_with(
        password, expected_hash
    )


def test_verify_password_success_with_update(password_authenticator):
    user_id, password = fake.pystr(), fake.pystr()
    expected_hash = fake.sha256()
    new_hash = fake.sha256()
    password_authenticator.authentication_persistence.get_password_hash = MagicMock(
        return_value=Ok(expected_hash)
    )
    password_authenticator.authentication_persistence.update_password_hash = MagicMock(
        return_value=Ok(None)
    )
    password_authenticator.crypto_context.verify_and_update = MagicMock(
        return_value=(True, new_hash)
    )
    assert password_authenticator.verify_password(user_id, password).unwrap() is None
    password_authenticator.authentication_persistence.get_password_hash.assert_called_once_with(
        user_id
    )
    password_authenticator.authentication_persistence.update_password_hash.assert_called_once_with(
        user_id, new_hash
    )
    password_authenticator.crypto_context.verify_and_update.assert_called_once_with(
        password, expected_hash
    )


def test_verify_password_fail_at_persistence(password_authenticator):
    user_id, password = fake.pystr(), fake.pystr()
    error = Err(fake.pystr())
    password_authenticator.authentication_persistence.get_password_hash = MagicMock(
        return_value=error
    )
    assert password_authenticator.verify_password(user_id, password) == error
    password_authenticator.crypto_context.verify_and_update.assert_not_called()
    password_authenticator.authentication_persistence.update_password_hash.assert_not_called()


@pytest.mark.parametrize("new_hash", [None, fake.sha256()])
def test_verify_password_fail_wrong_password(password_authenticator, new_hash):
    user_id, password = fake.pystr(), fake.pystr()
    expected_hash = fake.sha256()

    password_authenticator.authentication_persistence.get_password_hash = MagicMock(
        return_value=Ok(expected_hash)
    )

    password_authenticator.crypto_context.verify_and_update = MagicMock(
        return_value=(False, new_hash)
    )

    assert (
        password_authenticator.verify_password(user_id, password).unwrap_err()
        == f"Incorrect password "
        f"for user: {user_id}"
    )
    password_authenticator.authentication_persistence.get_password_hash.assert_called_once_with(
        user_id
    )
    password_authenticator.authentication_persistence.update_password_hash.assert_not_called()
    password_authenticator.crypto_context.verify_and_update.assert_called_once_with(
        password, expected_hash
    )
