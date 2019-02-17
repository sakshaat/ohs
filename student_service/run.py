from common.app_creation import create_app
from common.networking import find_free_port
from student_service.graphql_schema import schema

app = create_app(schema, "Student Service")
flask_app = app.flask_app

if __name__ == "__main__":
    flask_app.run(debug=True, port=find_free_port())
