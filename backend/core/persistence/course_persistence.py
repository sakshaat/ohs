from typing import Callable, List

import attr
from option import Err, Ok, Option, Result, maybe

from core.domain.course import Course, Section, SectionIdentity, Semester
from core.domain.user import Instructor


@attr.s
class CoursePersistence:
    """
    Persistence layer implementation for course related things.
    """

    # table courses(code text)
    get_connection = attr.ib(type=Callable)

    @property
    def connection(self):
        return self.get_connection()

    def create_course(self, course: Course) -> Result[Course, str]:
        if self.get_course(course.course_code):
            return Err(f"Course {course} already exists")
        c = self.connection.cursor()
        term = (course.course_code,)
        c.execute("INSERT INTO courses VALUES (%s)", term)
        self.connection.commit()
        return Ok(course)

    def delete_course(self, course_code: str) -> Result[str, str]:
        if not self.get_course(course_code):
            return Err(f"Course {course_code} does not exist")
        c = self.connection.cursor()
        c.execute("DELETE FROM courses WHERE course_code=%s", (course_code,))
        self.connection.commit()
        return Ok(course_code)

    def get_course(self, course_code: str) -> Option[Course]:
        c = self.connection.cursor()
        term = (course_code,)
        c.execute("SELECT * FROM courses WHERE course_code=%s", term)
        course = None
        res = c.fetchone()
        if res:
            course = Course(res[0])
        return maybe(course)

    def query_courses(self, filters=None) -> List[Course]:
        c = self.connection.cursor()
        if filters is None:
            c.execute("SELECT * FROM courses")
        elif "course_code" in filters:
            c.execute(
                "SELECT * FROM courses WHERE course_code=%s", (filters["course_code"])
            )
        courses = c.fetchall()
        if len(courses) > 0:
            courses = map(lambda x: Course(x[0]), courses)
        return list(courses)

    def create_section(self, section: Section) -> Result[Section, str]:
        if self.get_section(section.identity):
            return Err(f"Section {section} already exists")
        elif not self.get_course(section.course.course_code):
            return Err(f"Course {section.course} does not exist")
        else:
            c = self.connection.cursor()
            term = (
                section.course.course_code,
                section.year,
                section.semester.value,
                section.section_code,
                section.taught_by.user_name,
                section.num_students,
            )
            c.execute(
                "INSERT INTO sections(course, year, semester, section_code, taught_by, "
                "num_students) VALUES (%s, %s, %s, %s, %s, %s)",
                term,
            )
            self.connection.commit()
            return Ok(section)

    def get_section(self, section_identity: SectionIdentity) -> Option[Section]:
        c = self.connection.cursor()
        term = (
            section_identity.course.course_code,
            section_identity.year,
            str(section_identity.semester.value),
            section_identity.section_code,
        )

        c.execute(
            "SELECT * FROM sections WHERE course=%s AND year=%s AND semester=%s AND "
            "section_code=%s",
            term,
        )
        section = None
        res = c.fetchone()
        if res:

            def get_inst(user_name):
                c.execute(
                    "SELECT * FROM instructors WHERE user_name=%s", (str(user_name),)
                )
                res = c.fetchone()
                if res:
                    return Instructor(res[0], res[1], res[3])
                return None

            section = Section(
                Course(res[0]),
                res[1],
                Semester(int(res[2])),
                res[3],
                get_inst(res[4]),
                res[5],
            )
        return maybe(section)

    def query_sections(self, filters=None) -> List[Section]:
        c = self.connection.cursor()
        if filters is None:
            c.execute("SELECT * FROM sections")
        else:
            terms = []
            where_text = ""
            if "course_code" in filters:
                if where_text == "":
                    where_text += " WHERE"
                else:
                    where_text += " AND"
                where_text += " course=%s"
                terms.append(str(filters["course_code"]))
            if "year" in filters:
                if where_text == "":
                    where_text += " WHERE"
                else:
                    where_text += " AND"
                where_text += " year=%s"
                terms.append(str(filters["year"]))
            if "semester" in filters:
                if where_text == "":
                    where_text += " WHERE"
                else:
                    where_text += " AND"
                where_text += " semester=%s"
                terms.append(str(filters["semester"].value))
            if "section_code" in filters:
                if where_text == "":
                    where_text += " WHERE"
                else:
                    where_text += " AND"
                where_text += " section_code=%s"
                terms.append(filters["section_code"])
            if "taught_by" in filters:
                if where_text == "":
                    where_text += " WHERE"
                else:
                    where_text += " AND"
                where_text += " taught_by=%s"
                terms.append(filters["taught_by"].user_name)

            c.execute("SELECT * FROM sections" + where_text, tuple(terms))

        sections = c.fetchall()
        if len(sections) > 0:

            def get_inst(user_name):
                c.execute(f"SELECT * FROM instructors WHERE user_name='{user_name}'")
                res = c.fetchone()
                if res:
                    return Instructor(res[0], res[1], res[3])
                return None

            sections = map(
                lambda res: Section(
                    Course(res[0]),
                    res[1],
                    Semester(int(res[2])),
                    res[3],
                    get_inst(res[4]),
                    res[5],
                ),
                sections,
            )
        return list(sections)

    def delete_section(self, section: Section) -> Result[Section, str]:
        if not self.get_section(section):
            return Err(f"Section {section} does not exist")
        c = self.connection.cursor()
        term = (
            section.course.course_code,
            section.year,
            str(section.semester.value),
            section.section_code,
        )
        c.execute(
            "DELETE FROM sections WHERE course=%s AND year=%s AND semester=%s AND section_code=%s",
            term,
        )
        self.connection.commit()
        return Ok(section)
