import faker
from faker.providers import date_time, python

fake = faker.Faker()
fake.add_provider(python)
fake.add_provider(date_time)
