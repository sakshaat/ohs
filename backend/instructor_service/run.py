import os
import sys
from pathlib import Path

import flask
from flask import Flask
from flask_cors import CORS
from option import Err, Result

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
from core.persistence.connection_manager import ConnectionManager
from core.persistence.course_persistence import CoursePersistence
from core.persistence.instructor_persistence import InstructorPersistence


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
            ).flatmap(lambda instructor: self.get_token(user_id, password))

    def get_token(self, user_identity, password):
        return self.api.instructor_api.get_token(user_identity, password)

    def authenticate_user_by_token(self, token: str) -> Result[Instructor, str]:
        return self.api.instructor_api.verify_instructor_by_token(token)


flask_app = Flask("Instructor Service")
CORS(flask_app)
gql_controller = GraphqlController(
    build_schema([SchemaRestriction.ALL, SchemaRestriction.INSTRUCTOR])
)
course_persistence = CoursePersistence(lambda: flask.g.connection)
instructor_persistence = InstructorPersistence(lambda: flask.g.connection)

token_auth = JwtAuthenticator(os.environ["OHS_INSTRUCTOR_SERVICE_SECRET"])
password_auth = PasswordAuthenticator(instructor_persistence)

ohs_api = OhsApi(
    CourseApi(course_persistence),
    InstructorApi(instructor_persistence, password_auth, token_auth),
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
