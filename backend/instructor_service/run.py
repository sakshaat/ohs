import sys
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from option import Ok, Result

sys.path.insert(1, str(Path(__file__).parent.parent.resolve()))  # noqa

from core.api.course_api import CourseApi
from core.api.instructor_api import InstructorApi
from core.api.ohs_api import OhsApi
from core.app import App
from core.domain.user import Instructor
from core.gql.context import Context
from core.gql.graphql_controller import GraphqlController
from core.gql.schema_registry import SchemaRestriction, build_schema
from core.presistence.course_persistence import CoursePresistence


class InstructorService(App[Context]):
    def __init__(self, flask_app_, graphql_controller, api):
        self.api = api
        super().__init__(flask_app_, graphql_controller)

    def create_context(self, request) -> Context:
        return Context(self.api, self.authenticate_instructor(request).unwrap())

    def authenticate_instructor(self, request) -> Result[Instructor, str]:
        # TODO: implement authentication
        return Ok(None)


flask_app = Flask("Instructor Service")
CORS(flask_app)
gql_controller = GraphqlController(
    build_schema([SchemaRestriction.ALL, SchemaRestriction.INSTRUCTOR])
)
ohs_instructor_api = OhsApi(CourseApi(CoursePresistence()), InstructorApi())
app = InstructorService(flask_app, gql_controller, ohs_instructor_api)

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8000
    flask_app.run(debug=True, port=port)
