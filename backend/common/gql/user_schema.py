import graphene


class User(graphene.Interface):
    id = graphene.UUID(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)


class Instructor(graphene.ObjectType):
    class Meta:
        interfaces = (User,)

    @classmethod
    def from_domain(cls, domain_instructor):
        return cls(
            domain_instructor.id,
            domain_instructor.first_name,
            domain_instructor.last_name,
        )


class Student(graphene.ObjectType):
    class Meta:
        interfaces = (User,)

    student_number = graphene.String(required=True)
