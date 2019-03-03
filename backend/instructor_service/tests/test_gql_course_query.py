from unittest.mock import MagicMock

import pytest
from option import NONE, Some

from common.tests.generation import fake, list_fakes
from common.tests.generation.fake_course import fake_course, fake_section
from instructor_service.api.course_api import CourseApi
from instructor_service.gql.context import InstructorContext
from instructor_service.gql.graphql_schema import schema


class CourseQueryBehavious:
    mock_context = MagicMock(InstructorContext)
    mock_course_api = MagicMock(CourseApi)
    mock_context.api.course_api = mock_course_api

    def before_each(self):
        self.mock_get_method().reset_mock()
        self.mock_query_method().reset_mock()

    @property
    def query(self):
        raise NotImplementedError()

    @property
    def listing_query(self):
        raise NotImplementedError()

    @property
    def filters_list(self):
        raise NotImplementedError()

    def mock_get_method(self):
        raise NotImplementedError()

    def mock_query_method(self):
        raise NotImplementedError()

    def fake_domain(self):
        raise NotImplementedError()

    def get_code(self, fake_domain):
        raise NotImplementedError()

    def variables(self, code):
        raise NotImplementedError()

    def to_graphql(self, domain):
        raise NotImplementedError()

    def to_graphql_list(self, domain_list):
        raise NotImplementedError()

    def test_query_one(self):
        self.before_each()
        fake_domain = self.fake_domain()
        code = self.get_code(fake_domain)
        self.mock_get_method().return_value = Some(fake_domain)
        result = schema.execute(
            self.query, variables=self.variables(code), context=self.mock_context
        )
        assert not result.errors
        assert result.data == self.to_graphql(fake_domain)
        self.mock_get_method().assert_called_once_with(code)

    def test_query_one_empty(self):
        self.before_each()
        fake_domain = self.fake_domain()
        code = self.get_code(fake_domain)
        self.mock_get_method().return_value = NONE
        result = schema.execute(
            self.query, variables=self.variables(code), context=self.mock_context
        )
        assert not result.errors
        assert result.data == self.to_graphql(None)
        self.mock_get_method().assert_called_once_with(code)

    @pytest.mark.parametrize("num_objects", [0, 10])
    def test_listing(self, num_objects):
        for filters in self.filters_list:
            self.before_each()
            fake_domains = list_fakes(self.fake_domain, num_objects)
            self.mock_query_method().return_value = fake_domains
            variables = {"filters": filters} if filters else None
            result = schema.execute(
                self.listing_query, variables=variables, context=self.mock_context
            )
            assert result.data == self.to_graphql_list(fake_domains)
            self.mock_query_method().assert_called_once_with(filters)


class TestCourseQuery(CourseQueryBehavious):
    @property
    def query(self):
        return """
query getCourse($courseCode: String!) {
    course(courseCode: $courseCode) {
        courseCode
    }
}"""

    @property
    def listing_query(self):
        return """
query queryCourses($filters: String) {
    courses(filters: $filters) {
        courseCode
    }
}"""

    @property
    def filters_list(self):
        return [None, fake.pystr()]  # TODO: Use actual filters

    def mock_get_method(self):
        return self.mock_course_api.get_course

    def mock_query_method(self):
        return self.mock_course_api.query_courses

    def fake_domain(self):
        return fake_course()

    def get_code(self, fake_domain):
        return fake_domain.course_code

    def variables(self, code):
        return {"courseCode": code}

    def to_graphql(self, domain):
        if not domain:
            return {"course": None}
        return {"course": {"courseCode": domain.course_code}}

    def to_graphql_list(self, domain_list):
        return {
            "courses": [{"courseCode": course.course_code} for course in domain_list]
        }


class TestSectionQuery(CourseQueryBehavious):
    @property
    def query(self):
        return """
query getSection($sectionCode: String!) {
    section(sectionCode: $sectionCode) {
        course {
            courseCode
        }
        year
        semester
        sectionCode
        numStudents
    }
}"""

    @property
    def listing_query(self):
        return """
query querySections($filters: String) {
    sections(filters: $filters) {
        course {
            courseCode
        }
        year
        semester
        sectionCode
        numStudents
    }
}"""

    @property
    def filters_list(self):
        return [None, fake.pystr()]  # TODO: Use actual filters

    def mock_get_method(self):
        return self.mock_course_api.get_section

    def mock_query_method(self):
        return self.mock_course_api.query_sections

    def fake_domain(self):
        return fake_section()

    def get_code(self, fake_domain):
        return fake_domain.section_code

    def variables(self, code):
        return {"sectionCode": str(code)}

    def _to_gql(self, section):
        return {
            "course": {"courseCode": section.course.course_code},
            "year": section.year, 
            "semester": section.semester.name,
            "sectionCode": str(section.section_code),
            "numStudents": section.num_students,
        }

    def to_graphql(self, domain):
        if domain is None:
            return {"section": None}
        return {"section": self._to_gql(domain)}

    def to_graphql_list(self, domain_list):
        return {"sections": [self._to_gql(section) for section in domain_list]}
