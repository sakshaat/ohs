import pytest

from core.gql.schema_registry import SchemaRestriction, build_schema


@pytest.fixture
def schema():
    return build_schema(list(SchemaRestriction))
