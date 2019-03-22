import flask
from flask import Request
from option import Err, Ok, Result


class HttpError(ValueError):
    def __init__(self, code, *args):
        self.code = code
        super().__init__(*args)

    def to_dict(self):
        return {"errors": [str(s) for s in super().args]}

    def __repr__(self):
        return f"HttpError(code={self.code}, args={self.args})"

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.code == other.code
            and self.args == other.args
        )

    def to_flask_response(self):
        response = flask.jsonify(self.to_dict())
        response.status_code = self.code
        return response


def parse_auth_token(request: Request) -> Result[str, str]:
    """
    Parse a Bearer token from a request header
    Args:
        request:  The HTTP request

    Returns:
        The parsed token
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return Err("No 'Authorization' header")
    token_list = auth_header.split(" ")
    if len(token_list) != 2 or token_list[0] != "Bearer":
        return Err("Wrong Authorization header format (Bearer TOKEN)")
    return Ok(token_list[1])
