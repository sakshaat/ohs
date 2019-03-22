from typing import List, Callable

import attr
from option import Err, Ok, Option, Result, maybe

from core.domain.user import Student
from core.persistence.authentication_persistence import AuthenticationPersistence


@attr.s
class StudentPersistence(AuthenticationPersistence):
    """
    Persistence layer implementation for student related things.
    """

    get_connection = attr.ib(type=Callable)

    @property
    def connection(self):
        return self.get_connection()

    def create_student(
        self, student: Student, password_hash: str
    ) -> Result[Student, str]:
        if self.get_student(student.student_number):
            return Err(f"Student {student} already exists")
        c = self.connection.cursor()
        term = (
            student.first_name,
            student.last_name,
            password_hash,
            student.student_number,
        )
        c.execute(
            "INSERT INTO students(first_name, last_name, "
            "password_hash, student_number) VALUES (%s, %s, %s, %s)",
            term,
        )
        self.connection.commit()
        return Ok(student)

    # delete student
    def delete_student(self, student: Student) -> Result[Student, str]:
        if not self.get_student(student.student_number):
            return Err(f"Student {student} does not exist")
        c = self.connection.cursor()
        term = (student.student_number,)
        c.execute("DELETE FROM students WHERE student_number=%s", term)
        self.connection.commit()
        return Ok(student)

    # get student
    def get_student(self, user_identity: str) -> Option[Student]:
        c = self.connection.cursor()
        term = (user_identity,)
        c.execute("SELECT * FROM students WHERE student_number=%s", term)
        student = None
        res = c.fetchone()
        if res:
            student = Student(res[0], res[1], res[3])
        return maybe(student)

    def query_student(self, filters=None) -> List[Student]:
        c = self.connection.cursor()
        if filters is None:
            c.execute("SELECT * FROM students")
        else:
            terms = []
            where_text = ""
            if "student_number" in filters:
                if where_text == "":
                    where_text += " WHERE"
                else:
                    where_text += " AND"
                where_text += " student_number=%s"
                terms.append(filters["student_number"])
            if "first_name" in filters:
                if where_text == "":
                    where_text += " WHERE"
                else:
                    where_text += " AND"
                where_text += " first_name=%s"
                terms.append(filters["first_name"])
            if "last_name" in filters:
                if where_text == "":
                    where_text += " WHERE"
                else:
                    where_text += " AND"
                where_text += " last_name=%s"
                terms.append(filters["last_name"])
            c.execute("SELECT * FROM students" + where_text, tuple(terms))
        students = c.fetchall()
        if len(students) > 0:
            students = map(lambda res: Student(res[0], res[1], res[3]), students)
        return list(students)

    def get_password_hash(self, user_identity: str) -> Result[str, str]:
        c = self.connection.cursor()
        term = (user_identity,)
        c.execute("SELECT * FROM students WHERE student_number=%s", term)
        pass_hash = None
        res = c.fetchone()
        if res:
            pass_hash = res[2]
        else:
            return Err(f"Student {user_identity} does not exist")
        return maybe(pass_hash)

    def update_password_hash(
        self, user_identity: str, new_hash: str
    ) -> Result[None, str]:
        c = self.connection.cursor()
        term = (new_hash, user_identity)
        c.execute("UPDATE students SET password_hash=%s WHERE student_number=%s", term)
        self.connection.commit()
        return Ok(None)
