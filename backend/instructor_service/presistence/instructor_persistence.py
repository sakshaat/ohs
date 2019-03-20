from typing import Dict, List, Callable

import attr
from option import Err, Ok, Option, Result, maybe

from core.domain.user import User, Instructor
from core.presistence.authentication_presistence import AuthenticationPresistence


@attr.s
class InstructorPersistence(AuthenticationPresistence):
    """
    Presistence layer implementation for instructor related things.

    Dummy implementation for now, using Python dicts as the database.

    # TODO: Use an actual DB
    """

    get_connection = attr.ib(type=Callable)

    @property
    def connection(self):
        return self.get_connection()

    def create_instructor(
        self, instructor: Instructor, password_hash: str
    ) -> Result[Instructor, str]:
        if self.get_instructor(instructor.user_name):
            return Err(f"Instructor {instructor} already exists")
        c = self.connection.cursor()
        term = (
            instructor.first_name,
            instructor.last_name,
            password_hash,
            instructor.user_name,
        )
        c.execute(
            "INSERT INTO instructors(first_name, last_name, "
            "password_hash, user_name) VALUES (%s, %s, %s, %s)",
            term,
        )
        self.connection.commit()
        return Ok(instructor)

    # delete instructor
    def delete_instructor(self, instructor: Instructor) -> Result[Instructor, str]:
        if not self.get_instructor(instructor.user_name):
            return Err(f"Instructor {instructor} does not exist")
        c = self.connection.cursor()
        term = (instructor.user_name,)
        c.execute("DELETE FROM instructors WHERE user_name=%s", term)
        self.connection.commit()
        return Ok(instructor)

    # get instructor
    def get_instructor(self, user_identity: str) -> Option[Instructor]:
        c = self.connection.cursor()
        term = (user_identity,)
        c.execute("SELECT * FROM instructors WHERE user_name=%s", term)
        instructor = None
        res = c.fetchone()
        if res:
            instructor = Instructor(res[0])
        return maybe(instructor)

    def query_instructor(self, filters=None) -> List[Instructor]:
        c = self.connection.cursor()
        # TODO: filters
        c.execute("SELECT * FROM instructors")
        instructors = c.fetchall()
        if len(instructors) > 0:
            instructors = map(
                lambda res: Instructor(res[0], res[1], res[3]), instructors
            )
        return list(instructors)

    def get_password_hash(self, user_identity: str) -> Result[str, str]:
        c = self.connection.cursor()
        term = (user_identity,)
        c.execute("SELECT * FROM instructors WHERE user_name=%s", term)
        pass_hash = None
        res = c.fetchone()
        if res:
            pass_hash = res[2]
        else:
            return Err(f"Instructor {instructor} does not exist")
        return maybe(pass_hash)

    def update_password_hash(
        self, user_identity: str, new_hash: str
    ) -> Result[None, str]:
        c = self.connection.cursor()
        term = (new_hash, user_identity)
        c.execute("UPDATE instructors SET password_hash=%s WHERE user_name=%s")
        self.connection.commit()
        return Ok(None)
