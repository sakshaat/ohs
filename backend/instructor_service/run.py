import os
import sys
from pathlib import Path

from option import Err, Result

sys.path.insert(1, str(Path(__file__).parent.parent.resolve()))  # noqa
from core.app import App
from core.domain.user import Instructor
from core.gql.schema_registry import SchemaRestriction
from core.initialization import make_app


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


secret = os.environ["OHS_INSTRUCTOR_SERVICE_SECRET"]
app = make_app(
    InstructorService,
    "Instructor Service",
    secret,
    [SchemaRestriction.ALL, SchemaRestriction.INSTRUCTOR],
    Instructor,
)
flask_app = app.flask_app

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8000
    flask_app.run(debug=True, port=port)
