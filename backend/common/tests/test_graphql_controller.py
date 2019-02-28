from unittest.mock import MagicMock

from graphene import Schema

from common.gql.graphql_controller import GraphqlController
from common.gql.graphql_request import GraphqlRequest
from common.tests import FakeGraphqlResult

mock_schema = MagicMock(Schema)
controller = GraphqlController(mock_schema)


class TestExecute:
    fake_request = GraphqlRequest(query="{ q }", variables={"foo": "foo"})

    def test_success(self):
        expected_data = {"foo": "bar"}

        mock_schema.execute = MagicMock(
            return_value=FakeGraphqlResult(data=expected_data)
        )

        result = controller.execute(self.fake_request, None)

        assert result.unwrap() == {"data": expected_data}
        mock_schema.execute.assert_called_once_with(
            self.fake_request.query, variables=self.fake_request.variables, context=None
        )

    def test_errors(self):
        expected_errors = [ValueError("foo"), IndexError("bar")]

        mock_schema.execute = MagicMock(
            return_value=FakeGraphqlResult(errors=expected_errors)
        )

        result = controller.execute(self.fake_request, None)

        assert result.unwrap_err() == {"errors": [str(e) for e in expected_errors]}
        mock_schema.execute.assert_called_once_with(
            self.fake_request.query, variables=self.fake_request.variables, context=None
        )


class TestIntrospect:
    def test_success(self):
        expected_data = {"mmm": 122, "asd": [1, 3]}
        mock_schema.introspect = MagicMock(return_value=expected_data)

        result = controller.introspect()

        assert result.unwrap() == expected_data
        mock_schema.introspect.assert_called_once_with()

    def test_error(self):
        expected_error = ValueError("foo")
        mock_schema.introspect = MagicMock(side_effect=expected_error)

        result = controller.introspect()

        assert result.unwrap_err() == {"errors": [str(expected_error)]}
        mock_schema.introspect.assert_called_once_with()
