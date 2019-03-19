from typing import Callable, List, TypeVar

import faker
from faker.providers import date_time, misc, person, python

T = TypeVar("T")

fake = faker.Faker()
fake.add_provider(python)
fake.add_provider(date_time)
fake.add_provider(person)
fake.add_provider(misc)


def list_fakes(fake_fn: Callable[[], T], num: int) -> List[T]:
    return [fake_fn() for _ in range(num)]
