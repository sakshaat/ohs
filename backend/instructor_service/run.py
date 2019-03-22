import os
import sys
from pathlib import Path

import flask
from flask import Flask
from flask_cors import CORS
from option import Result, Err

sys.path.insert(1, str(Path(__file__).parent.parent.resolve()))  # noqa

from core.api.course_api import CourseApi
from core.api.instructor_api import InstructorApi
from core.api.ohs_api import OhsApi
from core.app import App
from core.authentication.password_auth import PasswordAuthenticator
from core.authentication.token_auth import JwtAuthenticator
from core.domain.user import Instructor
from core.gql.graphql_controller import GraphqlController
from core.gql.schema_registry import SchemaRestriction, build_schema
from core.http import parse_auth_token
from core.presistence.connection_manager import ConnectionManager
from core.presistence.course_persistence import CoursePresistence
from core.presistence.instructor_persistence import InstructorPersistence


class InstructorService(App):
    def create_user(self, post_json: dict):
        try:
            user_id = post_json["id"]
            password = post_json["password"]
            first_name = post_json["firstName"]
            last_name = post_json["lastName"]
        except KeyError:
            return Err("Invalid json body to create an instructor")
        else:
            return self.api.instructor_api.create_instructor(
                first_name, last_name, user_id, password
            )

    def get_token(self, user_identity, password):
        return self.api.instructor_api.get_token(user_identity, password)

    def authenticate_user_by_token(
        self, request: flask.Request
    ) -> Result[Instructor, str]:
        token = parse_auth_token(request)
        return token.flatmap(self.api.instructor_api.verify_instructor_by_token)


flask_app = Flask("Instructor Service")
CORS(flask_app)
gql_controller = GraphqlController(
    build_schema([SchemaRestriction.ALL, SchemaRestriction.INSTRUCTOR])
)
course_presistence = CoursePresistence(lambda: flask.g.connection)
instructor_presistence = InstructorPersistence(lambda: flask.g.connection)

token_auth = JwtAuthenticator(os.environ["OHS_INSTRUCTOR_SERVICE_SECRET"])
password_auth = PasswordAuthenticator(instructor_presistence)

ohs_api = OhsApi(
    CourseApi(course_presistence),
    InstructorApi(instructor_presistence, password_auth, token_auth),
)

connection_manager = ConnectionManager(
    1,
    100,
    {
        "host": os.getenv("OHS_DB_HOST"),
        "dbname": os.getenv("OHS_DB_NAME"),
        "user": os.getenv("OHS_DB_USER"),
        "password": os.getenv("OHS_DB_PASSWORD"),
    },
)
app = InstructorService(flask_app, gql_controller, ohs_api, connection_manager)

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8000
    flask_app.run(debug=True, port=port)
