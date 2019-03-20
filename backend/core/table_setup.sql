CREATE TABLE users (
 first_name VARCHAR (50) NOT NULL,
 last_name VARCHAR (50) NOT NULL,
 password_hash VARCHAR (50) NOT NULL,
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