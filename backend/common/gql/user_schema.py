import graphene


class User(graphene.Interface):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)


class Instructor(graphene.ObjectType):
    class Meta:
        interfaces = (User,)

    user_name = graphene.String(required=True)

    @classmethod
    def from_domain(cls, domain_instructor):
        return cls(
            domain_instructor.first_name,
            domain_instructor.last_name,
            domain_instructor.user_name,
        )


class Student(graphene.ObjectType):
    class Meta:
        interfaces = (User,)

    student_number = graphene.String(required=True)
