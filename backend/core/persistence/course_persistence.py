from typing import Callable, List
from uuid import UUID

import attr
from option import Err, NONE, Ok, Option, Result, maybe

from core.domain.course import (
    Course,
    OfficeHour,
    Section,
    SectionIdentity,
    Semester,
    Weekday,
)
from core.domain.user import Instructor
from core.persistence.meeting_persistence import MeetingPersistence


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
                terms.append(filters["taught_by"])

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

    def delete_section(
        self, section_identity: SectionIdentity
    ) -> Result[SectionIdentity, str]:
        if not self.get_section(section_identity):
            return Err(f"Section {section_identity} does not exist")
        c = self.connection.cursor()
        term = (
            section_identity.course.course_code,
            section_identity.year,
            str(section_identity.semester.value),
            section_identity.section_code,
        )
        c.execute(
            "DELETE FROM sections WHERE course=%s AND year=%s AND semester=%s AND section_code=%s",
            term,
        )
        self.connection.commit()
        return Ok(section_identity)

    def enroll_student(
        self, section: SectionIdentity, student_number: str
    ) -> Result[str, str]:
        c = self.connection.cursor()
        term = (student_number, section.to_string())
        c.execute(
            "INSERT INTO enrollment(student_number, section_id) VALUES (%s, %s)", term
        )
        self.connection.commit()
        return Ok(student_number)

    def get_sections_of_student(self, student_number: str) -> List[Section]:
        def to_section_identity(id):
            params = id.split(";delimiter;")
            return SectionIdentity(
                Course(params[0]), int(params[1]), Semester(int(params[2])), params[3]
            )

        c = self.connection.cursor()
        term = (student_number,)
        c.execute("SELECT * FROM enrollment WHERE student_number=%s", term)

        sections = c.fetchall()
        if len(sections) > 0:
            sections = map(
                lambda x: self.get_section(to_section_identity(x[1])).unwrap_or(None),
                sections,
            )
        return list(sections)

    def create_officehour(
        self, officehour: OfficeHour, mp: MeetingPersistence
    ) -> Result[OfficeHour, str]:
        if self.get_officehour(officehour.office_hour_id, mp):
            return Err(f"OfficeHour {officehour} already exists")
        c = self.connection.cursor()
        term = (
            str(officehour.office_hour_id),
            officehour.section.identity.to_string(),
            officehour.starting_hour,
            officehour.weekday.value,
        )
        c.execute(
            "INSERT INTO officehours(office_hour_id, section_id, starting_hour, day_of_week)"
            " VALUES (%s, %s, %s, %s)",
            term,
        )
        self.connection.commit()
        return Ok(officehour)

    def _res_to_officehour(self, res, mp) -> Option[OfficeHour]:
        def to_section_identity(id):
            params = id.split(";delimiter;")
            return SectionIdentity(
                Course(params[0]), int(params[1]), Semester(int(params[2])), params[3]
            )

        def format_meeting_slots(meeting_list):
            lst = [None, None, None, None, None, None]
            for meeting in meeting_list:
                lst[meeting.index] = meeting
            return lst

        office_hour_id = UUID(res[0])
        return self.get_section(to_section_identity(res[1])).map(
            lambda section: OfficeHour(
                office_hour_id,
                section,
                int(res[2]),
                Weekday(int(res[3])),
                format_meeting_slots(mp.get_meetings_of_officehour(office_hour_id)),
            )
        )

    def get_officehour(
        self, office_hour_id: UUID, mp: MeetingPersistence
    ) -> Option[OfficeHour]:
        c = self.connection.cursor()
        term = (str(office_hour_id),)
        c.execute("SELECT * FROM officehours WHERE office_hour_id=%s", term)
        officehour = NONE
        res = c.fetchone()
        if res:
            officehour = self._res_to_officehour(res, mp)
        return officehour

    def delete_officehour(
        self, office_hour_id: UUID, mp: MeetingPersistence
    ) -> Result[UUID, str]:
        if not self.get_officehour(office_hour_id, mp):
            return Err(f"OfficeHour {office_hour_id} does not exist")
        c = self.connection.cursor()
        c.execute(
            "DELETE FROM officehours WHERE office_hour_id=%s", (str(office_hour_id),)
        )
        self.connection.commit()
        return Ok(office_hour_id)

    def get_officehour_for_instructor_by_day(
        self, user_name: str, day: Weekday, mp: MeetingPersistence
    ) -> List[OfficeHour]:
        c = self.connection.cursor()
        officehours = []
        sections = list(
            map(
                lambda x: x.identity().to_string(),
                self.query_sections({"taught_by": user_name}),
            )
        )
        if len(sections) > 0:
            c.execute(
                "SELECT * FROM officehours WHERE day_of_week=%s AND (section_id=%s"
                + (" OR section_id=%s" * (len(sections) - 1))
                + ")",
                tuple([day.value] + sections),
            )
            results = c.fetchall()
            if len(results) > 0:
                officehours = list(
                    filter(
                        None,
                        (
                            self._res_to_officehour(res, mp).unwrap_or(None)
                            for res in results
                        ),
                    )
                )
        return officehours

    def get_officehour_for_section_by_day(
        self, section_identity: SectionIdentity, day: Weekday, mp: MeetingPersistence
    ) -> List[OfficeHour]:
        c = self.connection.cursor()
        officehours = []
        c.execute(
            "SELECT * FROM officehours WHERE day_of_week=%s AND section_id=%s",
            (day.value, section_identity.to_string()),
        )
        results = c.fetchall()
        if len(results) > 0:
            officehours = list(
                filter(
                    None,
                    (
                        self._res_to_officehour(res, mp).unwrap_or(None)
                        for res in results
                    ),
                )
            )
        return officehours
