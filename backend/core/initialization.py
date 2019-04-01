import os

import flask
from flask import Flask
from flask_cors import CORS

from core.api.course_api import CourseApi
from core.api.instructor_api import InstructorApi
from core.api.meeting_api import MeetingApi
from core.api.ohs_api import OhsApi
from core.api.student_api import StudentApi
from core.authentication.password_auth import PasswordAuthenticator
from core.authentication.token_auth import JwtAuthenticator
from core.gql.graphql_controller import GraphqlController
from core.gql.schema_registry import build_schema
from core.persistence.connection_manager import ConnectionManager
from core.persistence.course_persistence import CoursePersistence
from core.persistence.instructor_persistence import InstructorPersistence
from core.persistence.meeting_persistence import MeetingPersistence
from core.persistence.student_persistence import StudentPersistence


def get_connection():
    return flask.g.connection


def make_app(cls, name, secret, restrictions):
    flask_app = Flask(name)
    CORS(flask_app)
    gql_controller = GraphqlController(build_schema(restrictions))
    course_persistence = CoursePersistence(get_connection)
    instructor_persistence = InstructorPersistence(get_connection)
    student_persistence = StudentPersistence(get_connection)
    meeting_persistence = MeetingPersistence(get_connection)

    token_auth = JwtAuthenticator(secret)
    password_auth = PasswordAuthenticator(instructor_persistence)

    ohs_api = OhsApi(
        course_api=CourseApi(course_persistence, meeting_persistence),
        instructor_api=InstructorApi(instructor_persistence, password_auth, token_auth),
        student_api=StudentApi(student_persistence, password_auth, token_auth),
        meeting_api=MeetingApi(meeting_persistence),
    )

    connection_manager = ConnectionManager(
        1,
        100,
        {
            "host": os.getenv("OHS_DB_HOST"),
            "dbname": os.getenv("OHS_DB_NAME"),
            "user": os.getenv("OHS_DB_USER"),
            "password": os.getenv("OHS_DB_PASSWORD"),
        },
    )
    return cls(flask_app, gql_controller, ohs_api, connection_manager)
