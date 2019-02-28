import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).parent.parent.resolve()))  # noqa
from common.app import create_app
from common.networking import find_free_port
from instructor_service.gql.graphql_schema import schema

app = create_app(schema, "Instructor Service")
flask_app = app.flask_app

if __name__ == "__main__":
    flask_app.run(debug=True, port=find_free_port())
