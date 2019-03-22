from abc import ABCMeta, abstractmethod
from functools import wraps

import attr
import flask
from option import Err, Result

from core.api.ohs_api import OhsApi
from core.domain.user import User
from core.gql.context import Context
from core.gql.graphql_controller import GraphqlController
from core.gql.graphql_request import parse_graphql_request
from core.http import HttpError
from core.persistence.connection_manager import ConnectionManager


@attr.s(slots=True, auto_attribs=True)
class App(metaclass=ABCMeta):
    flask_app: flask.Flask
    graphql_controller: GraphqlController
    api: OhsApi
    connection_manager: ConnectionManager

    def __attrs_post_init__(self):
        self.setup_routes()

    def require_db(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with self.connection_manager.connect() as conn:
                flask.g.connection = conn
                result = f(*args, **kwargs)
            return result

        return wrapper

    def setup_routes(self):
        @self.flask_app.route("/graphql", methods=["GET", "POST"])
        @self.require_db
        def graphql():
            result = self.execute_gql(flask.request)
            if result.is_err:
                response = result.unwrap_err().to_flask_response()
            else:
                response = flask.jsonify(result.unwrap())
            return response

        @self.flask_app.route("/create-user", methods=["POST"])
        @self.require_db
        def create_user():
            request_json = flask.request.json
            if not request_json:
                return HttpError(400, "Not a valid JSON request").to_flask_response()
            creation_result = self.create_user(request_json)
            if creation_result.is_ok:
                return flask.jsonify({"token": creation_result.unwrap()})
            else:
                return HttpError(400, creation_result.unwrap_err()).to_flask_response()

        @self.flask_app.route("/get-token", methods=["POST"])
        @self.require_db
        def get_token():
            request_json = flask.request.json
            if not request_json:
                return HttpError(400, "Not a valid JSON request").to_flask_response()
            user_id = request_json.get("id")
            password = request_json.get("password")
            if user_id is None or password is None:
                return HttpError(400, "Invalid JSON body").to_flask_response()
            token_result = self.get_token(user_id, password)
            if token_result.is_ok:
                return flask.jsonify({"token": token_result.unwrap()})
            else:
                return HttpError(401, token_result.unwrap_err()).to_flask_response()

        @self.flask_app.route("/")
        def home():
            return "Hello"

    def create_secure_context(self, request: flask.Request) -> Result[Context, str]:
        return self.authenticate_user_by_token(request).map(
            lambda user: Context(self.api, user)
        )

    @abstractmethod
    def authenticate_user_by_token(self, request: flask.Request) -> Result[User, str]:
        pass

    @abstractmethod
    def create_user(self, post_json: dict) -> Result[str, str]:
        pass

    @abstractmethod
    def get_token(self, user_identity, password) -> Result[str, str]:
        pass

    def execute_gql(self, request: flask.Request) -> Result[dict, HttpError]:
        if request.method == "POST":
            gql_request = parse_graphql_request(request)
            if gql_request.is_err:
                return Err(HttpError(400, gql_request.unwrap_err()))
            return (
                self.create_secure_context(request)
                .map_err(lambda e: HttpError(401, e))
                .flatmap(
                    lambda ctx: self.graphql_controller.execute(
                        gql_request.unwrap(), ctx
                    ).map_err(lambda e: HttpError(400, e))
                )
            )
        else:
            return self.graphql_controller.introspect().map_err(
                lambda e: HttpError(400, e)
            )
