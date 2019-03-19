import sys
from pathlib import Path

from option import Ok, Result

sys.path.insert(1, str(Path(__file__).parent.parent.resolve()))  # noqa

from flask import Flask
from flask_cors import CORS

from instructor_service.api.course_api import CourseApi
from instructor_service.api.instructor_api import InstructorApi
from instructor_service.api.ohs_instructor_api import OhsInstructorApi
from instructor_service.gql.context import InstructorContext
from instructor_service.presistence.course_persistence import CoursePresistence

from core.app import App
from core.gql.graphql_controller import GraphqlController
from core.domain.user import Instructor
from instructor_service.gql.graphql_schema import schema


class InstructorService(App[InstructorContext]):
    def __init__(self, flask_app_, graphql_controller, api):
        self.api = api
        super().__init__(flask_app_, graphql_controller)

    def create_context(self, request) -> InstructorContext:
        return InstructorContext(
            self.api, self.authenticate_instructor(request).unwrap()
        )

    def authenticate_instructor(self, request) -> Result[Instructor, str]:
        # TODO: implement authentication
        return Ok(None)


flask_app = Flask("Instructor Service")
CORS(flask_app)
gql_controller = GraphqlController(schema)
ohs_instructor_api = OhsInstructorApi(CourseApi(CoursePresistence()), InstructorApi())
app = InstructorService(flask_app, gql_controller, ohs_instructor_api)

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8000
    flask_app.run(debug=True, port=port)
