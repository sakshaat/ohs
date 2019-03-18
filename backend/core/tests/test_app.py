from unittest.mock import MagicMock

import pytest
from flask import Flask, Request
from option import Result
from pathlib import Path

from core.app import App
from core.gql.graphql_controller import GraphqlController
from core.gql.graphql_request import GraphqlRequest

mock_gql_controller = MagicMock(GraphqlController)
mock_flask_app = MagicMock(Flask)


class FakeApp(App[None]):
    def create_context(self, request):
        return None


db_path = str(Path(__file__).parent.parent / Path("common", "database.ini"))
app = FakeApp(mock_flask_app, mock_gql_controller, db_path)


class TestExecuteGql:
    def test_post_success(self):
        expected_data = {"data": {"f": "s"}}
        query = "foo"

        request = MagicMock(Request)
        request.method = "POST"
        request.json = {"query": query}

        gql_request = GraphqlRequest(query)

        mock_gql_controller.execute = MagicMock(return_value=Result.Ok(expected_data))
        result = app.execute_gql(request)
        assert result.unwrap() == expected_data
        mock_gql_controller.execute.assert_called_once_with(
            gql_request, app.create_context(...)
        )

    def test_post_parse_fail(self):
        request = MagicMock(Request)
        request.method = "POST"
        request.json = None

        mock_gql_controller.execute = MagicMock()

        result = app.execute_gql(request)
        for err in result.unwrap_err()["errors"]:
            assert isinstance(err, str)
        mock_gql_controller.execute.assert_not_called()

    @pytest.mark.parametrize(
        "expected_result", [Result.Ok({"foo": "bar"}), Result.Err({"bar": "qux"})]
    )
    def test_get(self, expected_result):
        request = MagicMock(Request)
        request.method = "GET"

        mock_gql_controller.introspect = MagicMock(return_value=expected_result)
        result = app.execute_gql(request)

        assert result == expected_result
        mock_gql_controller.introspect.assert_called_once_with()
