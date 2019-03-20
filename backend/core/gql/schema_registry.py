from collections import defaultdict
from enum import Enum, auto
from itertools import chain
from typing import List

import graphene
from graphene.utils.str_converters import to_snake_case


class SchemaRestriction(Enum):
    INSTRUCTOR = auto()
    STUDENT = auto()
    ALL = auto()


_query_registry = defaultdict(list)
_mutation_registry = defaultdict(list)


def register_query(allow):
    def wrapper(cls):
        _query_registry[allow].append(cls)
        return cls

    return wrapper


def register_mutation(allow):
    def wrapper(cls):
        _mutation_registry[allow].append(cls)
        return cls

    return wrapper


def build_schema(allowed_list: List[SchemaRestriction]):
    allowed_queries = chain(
        *(
            query_lst
            for allow, query_lst in _query_registry.items()
            if allow in allowed_list
        )
    )
    allowed_mutations = list(
        chain(
            *(
                mutation_lst
                for allow, mutation_lst in _mutation_registry.items()
                if allow in allowed_list
            )
        )
    )

    class Query(*allowed_queries):
        pass

    if allowed_mutations:
        Mutation = type(
            "Mutation",
            (graphene.ObjectType,),
            {
                to_snake_case(mutation.__name__): mutation.Field()
                for mutation in allowed_mutations
            },
        )

        return graphene.Schema(query=Query, mutation=Mutation)
    return graphene.Schema(query=Query)
