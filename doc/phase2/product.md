# What was built

# High level design

Our frontend is built with React, (fill more stuff below)
    
Our backend is built with Python. It is a GraphQL API built on top of [Graphene](https://graphene-python.org/) served by [Flask](http://flask.pocoo.org/).
It is split into two parts: Instructor service and Student service.

We are following a [domain driven design](https://en.wikipedia.org/wiki/Domain-driven_design) + [ports and adapters](http://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) architecture, 
the reason for this approach is that each individual components is testable on its own, without depending on any other components. For example, 
in this fairy involved [test file](https://github.com/office-hour-scheduler/ohs/blob/master/backend/core/tests/graphql/test_course_mutations.py), we are able to mock out any classes that is not under testing.

The only data type that can cross boundries in our application are domain objects, hence the "ports and adapters". (port can only accept domain objects, adapters converts layer local data to domain data).
This allows us to swap out any components of our application without affecting the other parts.

Another advantage of this design is that we are deferring all state to our persistence layer and keeping no state at all in our application. This means our application
is highly scaleable, with the database being its only bottleneck.

# Technical highlights

GraphQL is our team's main interest when we started this project, but its steep learning curve has proven to be somewhat troublesome in the actual implementation of our application.
Despite the slower progress in implementing features, we believe that learning GraphQL is very beneficial to us, since it is a very useful tool in a developer's tool belt.

In our backend, we are using the [Option](https://pypi.org/project/option/) library to represent None objects and exceptions. By using `Option` and `Result` types, in combination
with extensive usage of [type hinting](https://www.python.org/dev/peps/pep-0560/), we are able to write more type safe code than a typical Python program, at the cost of code being
too terse from time to time (Example: https://github.com/office-hour-scheduler/ohs/blob/master/backend/core/app.py#L103).

For user authentication, we are using a combination of username/password and JWT. A user would first log in with their username and password to obain a token, and use that token
to make authenticated requests to our GraphQL endpoint. (More details here: https://github.com/office-hour-scheduler/ohs/wiki/How-to-create-a-new-user-and-authenticate-for-GraphQL-access)
For the instructor service and student services, they are exposing a subset of our entire GraphQL schema to ensure a student cannot perform instructor actions, while still being
able to perform common actions shared between the two user types, and vice versa. Since the entire GraphQL end point required authenticated requests, we don't have to check
for user type in the actual query operations.

We are using docker-compose for deployment (compose file here: https://github.com/office-hour-scheduler/ohs/blob/master/docker-compose.yml), and our application is configured with
environment variables. docker-compose enables us to deploy and update all components of our application, including the database, with one command. And the use of environment
variables works nicely with docker, and simplfies reading configurations in actual code (No need to fight with file paths anymore)

# Process

We are roughly following a Kanban development methodology, since it's not very realistic for us to have sprints. Our Kanban board can be found here: https://github.com/office-hour-scheduler/ohs/projects/1

We are using our [GitHub repo wiki](https://github.com/office-hour-scheduler/ohs/wiki) to note things that are useful for developers to reduce communication overhead.

# Triage