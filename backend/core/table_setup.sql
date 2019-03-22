CREATE TABLE users (
 first_name VARCHAR (50) NOT NULL,
 last_name VARCHAR (50) NOT NULL,
 password_hash TEXT NOT NULL,
 PRIMARY KEY (first_name, last_name)
);

CREATE TABLE instructors (
 user_name VARCHAR (50) PRIMARY KEY
) INHERITS (users);

CREATE TABLE students (
 student_number VARCHAR (50) PRIMARY KEY
) INHERITS (users);

CREATE TABLE courses (
 course_code VARCHAR (50) PRIMARY KEY
);

CREATE TABLE sections(
 course VARCHAR (50) NOT NULL,
 year integer NOT NULL,
 semester VARCHAR (50) NOT NULL,
 section_code VARCHAR (50) NOT NULL,
 taught_by VARCHAR (50) NOT NULL,
 num_students integer NOT NULL,
 PRIMARY KEY (course, year, semester, section_code),
 CONSTRAINT course_fkey FOREIGN KEY (course)
    REFERENCES courses (course_code) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
 CONSTRAINT instructor_fkey FOREIGN KEY (taught_by)
    REFERENCES instructors (user_name) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE meetings (
 meeting_id VARCHAR (50) PRIMARY KEY,
 instructor VARCHAR (50) NOT NULL,
 student VARCHAR (50) NOT NULL,
 start_time VARCHAR (50) NOT NULL,
 end_time VARCHAR (50) NOT NULL,
 CONSTRAINT instructor_fkey FOREIGN KEY (instructor)
    REFERENCES instructors (user_name) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
 CONSTRAINT student_fkey FOREIGN KEY (student)
    REFERENCES students (student_number) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE notes (
 note_id VARCHAR (50) PRIMARY KEY,
 meeting_id VARCHAR (50) NOT NULL,
 time_stamp VARCHAR (50) NOT NULL,
 content_text TEXT,
 CONSTRAINT meeting_fkey FOREIGN KEY (meeting_id)
    REFERENCES meetings (meeting_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION 
);

CREATE TABLE comments (
 comment_id VARCHAR (50) PRIMARY KEY,
 meeting_id VARCHAR (50) NOT NULL,
 author_if_instructor VARCHAR (50),
 author_if_student VARCHAR (50),
 time_stamp VARCHAR (50) NOT NULL,
 content_text TEXT,
 CONSTRAINT meeting_fkey FOREIGN KEY (meeting_id)
    REFERENCES meetings (meeting_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
 CONSTRAINT has_author CHECK (
      CASE WHEN author_if_instructor IS NULL THEN 0 ELSE 1 END +
      CASE WHEN author_if_student  IS NULL THEN 0 ELSE 1 END = 1
    )
);
