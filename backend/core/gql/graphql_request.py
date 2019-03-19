from typing import NamedTuple

import flask
from option import Result


class GraphqlRequest(NamedTuple):
    query: str
    variables: dict = None


def parse_graphql_request(request: flask.Request) -> Result[GraphqlRequest, str]:
    request_json = request.json
    if not request_json:
        return Result.Err("Not a valid JSON request")
    query = request_json.get("query")
    if not query:
        return Result.Err("Could not find GraphQL query for request")
    variables = request_json.get("variables")
    return Result.Ok(GraphqlRequest(query, variables))
