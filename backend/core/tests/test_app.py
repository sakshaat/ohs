from unittest.mock import MagicMock

import pytest
from flask import Flask, Request
from option import Err, Ok, Result

from core.api.ohs_api import OhsApi
from core.app import App
from core.gql.graphql_controller import GraphqlController
from core.gql.graphql_request import GraphqlRequest
from core.http import HttpError
from core.persistence.connection_manager import ConnectionManager
from core.tests.generation import fake

mock_gql_controller = MagicMock(GraphqlController)
mock_flask_app = MagicMock(Flask)
mock_connection_manager = MagicMock(ConnectionManager)
mock_api = MagicMock(OhsApi)


class FakeApp(App):
    def create_user(self, post_json: dict) -> Result[str, str]:
        pass

    def get_token(self, user_identity, password) -> Result[str, str]:
        pass

    authenticate_user_by_token = MagicMock(return_value=Ok(None))


app = FakeApp(mock_flask_app, mock_gql_controller, mock_api, mock_connection_manager)


class TestExecuteGql:
    @pytest.mark.parametrize("success", [True, False])
    def test_post(self, success):
        expected_data = {"data": {"f": "s"}}
        query = "foo"

        request = MagicMock(Request)
        request.method = "POST"
        request.json = {"query": query}

        gql_request = GraphqlRequest(query)

        result = Ok(expected_data) if success else Err(expected_data)
        mock_gql_controller.execute = MagicMock(return_value=result)

        result = app.execute_gql(request)
        if success:
            assert result.unwrap() == expected_data
        else:
            assert result.unwrap_err() == HttpError(400, expected_data)
        mock_gql_controller.execute.assert_called_once_with(
            gql_request, app.create_secure_context(...).unwrap()
        )

    def test_post_parse_fail(self):
        request = MagicMock(Request)
        request.method = "POST"
        request.json = None

        mock_gql_controller.execute = MagicMock()

        result = app.execute_gql(request)
        assert result.unwrap_err().code == 400
        for err in result.unwrap_err().to_dict()["errors"]:
            assert isinstance(err, str)
        mock_gql_controller.execute.assert_not_called()

    def test_post_auth_fail(self):
        request = MagicMock(Request)
        request.method = "POST"
        request.json = {"query": "bar"}
        error = fake.pystr()

        mock_gql_controller.execute = MagicMock()
        _old_create_secure_context = app.create_secure_context
        app.create_secure_context = MagicMock(return_value=Err(error))
        result = app.execute_gql(request)
        assert result.unwrap_err().code == 401
        assert result.unwrap_err().to_dict() == {"errors": [error]}

        mock_gql_controller.execute.assert_not_called()
        app.create_secure_context = _old_create_secure_context

    @pytest.mark.parametrize(
        "expected_result", [Result.Ok({"foo": "bar"}), Result.Err({"bar": "qux"})]
    )
    def test_get(self, expected_result):
        request = MagicMock(Request)
        request.method = "GET"

        mock_gql_controller.introspect = MagicMock(return_value=expected_result)
        result = app.execute_gql(request)

        if result.is_err:
            assert result.unwrap_err() == HttpError(400, expected_result.unwrap_err())
        else:
            assert result.unwrap()["data"] == expected_result.unwrap()
        mock_gql_controller.introspect.assert_called_once_with()
