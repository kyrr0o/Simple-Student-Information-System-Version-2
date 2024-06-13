DROP DATABASE IF EXISTS student_information_system;
CREATE DATABASE student_information_system;

USE student_information_system;

CREATE TABLE courses (
    course_title VARCHAR(50),
    course_code VARCHAR(10) PRIMARY KEY
);

CREATE TABLE students (
    idNum VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender ENUM('Male', 'Female'),
    course_code VARCHAR(10),
    yearLevel VARCHAR(10),
    FOREIGN KEY (course_code) REFERENCES courses(course_code) ON DELETE SET NULL
);

INSERT INTO Courses (course_code, course_title) VALUES
('BSCS', 'BS-COMPUTER SCIENCE'),
('BSCA', 'BS-COMPUTER APPLICATIONS'),
('BSIS', 'BS-INFORMATION SYSTEM'),
('BSIT', 'BS-INFORMATION TECHNOLOGY');

INSERT INTO students (idNum, first_name, last_name, gender, course_code, yearLevel) VALUES
('2021-1756', 'Kaycee', 'Nalzaro', 'Female', 'BSCS', '1'),
('2021-1746', 'Nikki', 'Robles', 'Female', 'BSCS', '1'),
('2021-1736', 'Justine', 'Vergara', 'Male', 'BSCS', '1');
