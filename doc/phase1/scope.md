Our main learning goal for this project is to become familiar with GraphQL, since it’s a new and powerful way to design an API. All of us are already familiar with REST, so a new technology like this would be beneficial to learn. Most of us are also hoping that GraphQL skills will be useful in future job searches.

Originally we did not agree on our learning goals. We floated the idea of possibly building a backend from scratch in C and having only a very minimal frontend, but we discarded that idea because we thought it would take too long to get an initial vertical slice working. We also considered writing our backend in a web framework for Rust, but discarded that idea for similar reasons. Ultimately, we had two options; we were either going to learn the syntax for GraphQL, or we were going to use technologies we were already familiar with (Django and React), but spend a lot of time building a nice user interface. We opted for GraphQL, because it seemed like even after putting in time to learn it, we probably would still have enough time to build out a nice user interface.


GraphQL is an API query language which handles the public interface of the backend for us. We can focus on implementation of business logic and UI. From this, we can select use-cases with emphasis on backend behaviour rather than worrying about how the endpoints are exposed. GraphQL also allows us to use many different API queries since it is flexible on what requests it accepts.
 
We will begin by implementing the following Instructor use cases:

- Add courses
- Create / Delete lecture sections (Section)
- C / R / U / D Office Hours with each Section
- Split each Office Hour into Slots (automatic - no UI interaction)
- View / Edit / Delete an already booked Meeting
- Add comments to an existing Meeting
- Add notes to a student (may or may not be associated with a meeting)

… and Student use cases:
- View office hour slots for lecture sections you are enrolled in (can see if they are booked)
- Book a slot for a meeting
- Add comments to an existing meeting
 
After all the core use cases described above are finished, these are our lower priority use cases:
- Calender integration
- Reminders when a meeting is coming up/almost done
- “Sorry I’m Late” notification

Furthermore, the following are explicitly out of scope:
- Anything to do with TAs, and user management (the only users in our application are the professor, and students which come pre-populated in the database)
- Associate students with lecture sections (existing student accounts are by default associated with all lecture sections / all courses in the system)

Overall, our design will stay as close as possible to the use-cases outlined on the midterm, and our features will focus on fulfilling them.

