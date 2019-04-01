import os
import sys
from pathlib import Path

from option import Err, Result

sys.path.insert(1, str(Path(__file__).parent.parent.resolve()))  # noqa
from core.app import App
from core.domain.user import User
from core.gql.schema_registry import SchemaRestriction
from core.initialization import make_app


class StudentService(App):
    def authenticate_user_by_token(self, token: str) -> Result[User, str]:
        return self.api.student_api.verify_student_by_token(token)

    def create_user(self, post_json: dict) -> Result[str, str]:
        try:
            user_id = post_json["id"]
            password = post_json["password"]
            first_name = post_json["firstName"]
            last_name = post_json["lastName"]
        except KeyError:
            return Err("Invalid json body to create a student")
        else:
            return self.api.student_api.create_student(
                first_name, last_name, user_id, password
            ).flatmap(lambda student: self.get_token(user_id, password))

    def get_token(self, user_identity, password) -> Result[str, str]:
        return self.api.student_api.get_token(user_identity, password)


secret = os.environ["OHS_STUDENT_SERVICE_SECRET"]
app = make_app(
    StudentService,
    "Student Service",
    secret,
    [SchemaRestriction.ALL, SchemaRestriction.STUDENT],
)
flask_app = app.flask_app
if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8001
    flask_app.run(debug=True, port=port)
