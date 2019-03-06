import sys
from pathlib import Path

import flask

sys.path.insert(1, str(Path(__file__).parent.parent.resolve()))  # noqa

from flask import Flask
from flask_cors import CORS

from instructor_service.api.course_api import CourseApi
from instructor_service.api.ohs_instructor_api import OhsInstructorApi
from instructor_service.gql.context import InstructorContext
from instructor_service.presistence.course_persistence import CoursePresistence

from common.app import App
from common.gql.graphql_controller import GraphqlController
from instructor_service.gql.graphql_schema import schema


class InstructorService(App[InstructorContext]):
    def __init__(self, flask_app_, graphql_controller, database_path, api):
        self.api = api
        super().__init__(flask_app_, graphql_controller, database_path)

    def create_context(self, request) -> InstructorContext:
        return InstructorContext(self.api)


flask_app = Flask("Instructor Service")
CORS(flask_app)
gql_controller = GraphqlController(schema)
course_presistence = CoursePresistence(lambda: flask.g.connection)
ohs_instructor_api = OhsInstructorApi(CourseApi(course_presistence))
db_path = str(Path(__file__).parent.parent / Path("common", "main.db"))
app = InstructorService(flask_app, gql_controller, db_path, ohs_instructor_api)

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8000
    flask_app.run(debug=True, port=port)
