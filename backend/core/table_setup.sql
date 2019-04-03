CREATE TABLE users
(
  first_name    VARCHAR(200) NOT NULL,
  last_name     VARCHAR(200) NOT NULL,
  password_hash TEXT        NOT NULL,
  PRIMARY KEY (first_name, last_name)
);

CREATE TABLE instructors
(
  user_name VARCHAR(200) PRIMARY KEY
) INHERITS (users);

CREATE TABLE students
(
  student_number VARCHAR(200) PRIMARY KEY
) INHERITS (users);

CREATE TABLE courses
(
  course_code VARCHAR(200) PRIMARY KEY
);

CREATE TABLE sections
(
  course       VARCHAR(200) NOT NULL,
  year         integer     NOT NULL,
  semester     VARCHAR(200) NOT NULL,
  section_code VARCHAR(200) NOT NULL,
  taught_by    VARCHAR(200) NOT NULL,
  num_students integer     NOT NULL,
  PRIMARY KEY (course, year, semester, section_code),
  CONSTRAINT course_fkey FOREIGN KEY (course)
    REFERENCES courses (course_code) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT instructor_fkey FOREIGN KEY (taught_by)
    REFERENCES instructors (user_name) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE officehours
(
  office_hour_id        VARCHAR(200) PRIMARY KEY,
  section_id           VARCHAR(200) NOT NULL,
  starting_hour        integer NOT NULL,
  day_of_week          integer NOT NULL
);

CREATE TABLE meetings
(
  meeting_id      VARCHAR(200) PRIMARY KEY,
  office_hour_id  VARCHAR(200) NOT NULL,
  index           integer     NOT NULL,
  instructor      VARCHAR(200) NOT NULL,
  student         VARCHAR(200) NOT NULL,
  start_time      BIGINT      NOT NULL,
  CONSTRAINT instructor_fkey FOREIGN KEY (instructor)
    REFERENCES instructors (user_name) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT student_fkey FOREIGN KEY (student)
    REFERENCES students (student_number) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT officehour_fkey FOREIGN KEY (office_hour_id)
    REFERENCES officehours (office_hour_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT no_overlap_slot UNIQUE(office_hour_id, index)
);

CREATE TABLE notes
(
  note_id      VARCHAR(200) PRIMARY KEY,
  meeting_id   VARCHAR(200) NOT NULL,
  time_stamp   BIGINT      NOT NULL,
  content_text TEXT,
  CONSTRAINT meeting_fkey FOREIGN KEY (meeting_id)
    REFERENCES meetings (meeting_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE comments
(
  comment_id           VARCHAR(200) PRIMARY KEY,
  meeting_id           VARCHAR(200) NOT NULL,
  author_if_instructor VARCHAR(200),
  author_if_student    VARCHAR(200),
  time_stamp           BIGINT      NOT NULL,
  content_text         TEXT,
  CONSTRAINT meeting_fkey FOREIGN KEY (meeting_id)
    REFERENCES meetings (meeting_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT has_author CHECK (
        CASE WHEN author_if_instructor IS NULL THEN 0 ELSE 1 END +
        CASE WHEN author_if_student IS NULL THEN 0 ELSE 1 END = 1
    )
);

CREATE TABLE enrollment
(
  student_number       VARCHAR(200) NOT NULL,
  section_id           VARCHAR(200) NOT NULL,
  PRIMARY KEY (student_number, section_id),
  CONSTRAINT student_fkey FOREIGN KEY (student_number)
    REFERENCES students (student_number) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
);
