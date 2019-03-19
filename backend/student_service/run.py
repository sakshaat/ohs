import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).parent.parent.resolve()))  # noqa

from flask import Flask

from core.app import App
from core.gql.graphql_controller import GraphqlController
from student_service.gql.graphql_schema import schema


class StudentService(App):
    def __init__(self, flask_app_, graphql_controller):
        super().__init__(flask_app_, graphql_controller)

    def create_context(self, request):
        pass


flask_app = Flask("Student Service")
gql_controller = GraphqlController(schema)
app = StudentService(flask_app, gql_controller)

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8001
    flask_app.run(debug=True, port=port)
