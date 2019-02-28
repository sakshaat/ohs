from typing import Callable, List, TypeVar

import faker
from faker.providers import date_time, python

T = TypeVar("T")

fake = faker.Faker()
fake.add_provider(python)
fake.add_provider(date_time)


def list_fakes(fake_fn: Callable[[], T], num: int) -> List[T]:
    return [fake_fn() for _ in range(num)]
