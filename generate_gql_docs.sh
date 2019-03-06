#!/usr/bin/env bash
set -e
INSTRUCTOR_SCHEMA_PATH="./doc/instructor_schema"
graphidocs -e http://localhost:8000/graphql -o $INSTRUCTOR_SCHEMA_PATH --force
echo "Instructor schema documentation generated at: $INSTRUCTOR_SCHEMA_PATH"
