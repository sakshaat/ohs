import sys
from pathlib import Path

from flask import Flask

sys.path.insert(1, str(Path(__file__).parent.parent.resolve()))  # noqa

from core.app import App
from core.gql.graphql_controller import GraphqlController
from core.gql.schema_registry import SchemaRestriction, build_schema


class StudentService(App):
    def __init__(self, flask_app_, graphql_controller):
        super().__init__(flask_app_, graphql_controller)

    def create_context(self, request):
        pass


flask_app = Flask("Student Service")
gql_controller = GraphqlController(
    build_schema([SchemaRestriction.ALL, SchemaRestriction.STUDENT])
)
app = StudentService(flask_app, gql_controller)

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8001
    flask_app.run(debug=True, port=port)
