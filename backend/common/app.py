import attr
import flask
from graphene import Schema
from option import Result

from common.gql.graphql_controller import GraphqlController
from common.gql.graphql_request import parse_graphql_request


@attr.s(slots=True, auto_attribs=True)
class App:
    flask_app: flask.Flask
    graphql_controller: GraphqlController

    def execute_gql(self, request: flask.Request) -> Result[dict, dict]:
        if request.method == "POST":
            gql_request = parse_graphql_request(request)
            return gql_request.map_err(lambda e: {"errors": [e]}).flatmap(
                self.graphql_controller.execute
            )
        else:
            return self.graphql_controller.introspect()


def create_app(schema: Schema, name: str = None) -> App:
    flask_app = flask.Flask(name or __name__, instance_relative_config=True)
    graphql_controller = GraphqlController(schema)
    app = App(flask_app, graphql_controller)

    @flask_app.route("/graphql", methods=["GET", "POST"])
    def graphql():
        result = app.execute_gql(flask.request)
        if result.is_err:
            response = flask.jsonify(result.unwrap_err())
            response.status_code = 400
        else:
            response = flask.jsonify(result.unwrap())
        return response

    return app
