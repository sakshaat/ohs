#!/usr/bin/env bash
set -e
INSTRUCTOR_SCHEMA_PATH="./doc/instructor_schema"
wget "http://127.0.0.1:8000/graphql" -O ./${INSTRUCTOR_SCHEMA_PATH}.json
graphidocs -s ${INSTRUCTOR_SCHEMA_PATH}.json -o $INSTRUCTOR_SCHEMA_PATH --force
echo "Instructor schema documentation generated at: $INSTRUCTOR_SCHEMA_PATH"

STUDENT_SCHEMA_PATH="./doc/student_schema"
wget "http://127.0.0.1:8001/graphql" -O ./${STUDENT_SCHEMA_PATH}.json
graphidocs -s ${STUDENT_SCHEMA_PATH}.json -o $STUDENT_SCHEMA_PATH --force
echo "Student schema documentation generated at: $STUDENT_SCHEMA_PATH"
