CREATE TABLE sys.users (
  id int PRIMARY KEY auto_increment,
  user_name varchar(30) NOT NULL,
  user_password varchar(30) NOT NULL,
  person_id int
);


CREATE TABLE sys.universities (
  id int PRIMARY KEY auto_increment,
  university_name varchar(30) NOT NULL
);

INSERT INTO sys.universities (university_name) VALUES ('University of Leeds');

CREATE TABLE sys.courses (
  id int PRIMARY KEY auto_increment,
  course_name varchar(30) NOT NULL,
  qualification_code varchar(15) NOT NULL
);

INSERT INTO sys.courses (course_name, qualification_code) VALUES ('Computer Science', 'BSc');

SELECT * FROM sys.uni_courses;

DROP TABLE sys.uni_courses;

CREATE TABLE sys.uni_courses (
  id int PRIMARY KEY auto_increment,
  uni_id int NOT NULL,
  course_id int NOT NULL,
  active_mkr varchar(1) NOT NULL,
  req_grade_one varchar(5) NOT NULL,
  req_grade_two varchar(5) NOT NULL,
  req_grade_three varchar(5) NOT NULL,
  req_grade_four varchar(5),
  req_subject_one int,
  req_sub_one_grade varchar(5),
  req_subject_two int,
  req_sub_two_grade varchar(5),
  FOREIGN KEY (uni_id) references universities(id),
  FOREIGN KEY (course_id) references courses(id),
  FOREIGN KEY (req_subject_one) references required_subjects(id),
  FOREIGN KEY (req_subject_two) references required_subjects(id)
);

INSERT INTO sys.uni_courses (uni_id, course_id, active_mkr, req_grade_one, req_grade_two, req_grade_three, req_subject_one, req_sub_one_grade, req_subject_two, req_sub_two_grade) VALUES (1, 1, 'Y', 'A', 'A', 'A', 1, 'A', 2, 'A');

DELETE FROM sys.uni_courses WHERE id = 1;

CREATE TABLE sys.required_subjects(
  id int PRIMARY KEY auto_increment,
  subject_name VARCHAR(100) NOT NULL,
  subject_level VARCHAR(1) NOT NULL
);

INSERT INTO sys.required_subjects (subject_name, subject_level) VALUES ('Mathematics', 'A');
INSERT INTO sys.required_subjects (subject_name, subject_level) VALUES ('Computer Science', 'A');

SELECT * FROM sys.uni_course_keyterms;

DELETE FROM sys.uni_course_keyterms WHERE uni_course_id = 1;

INSERT INTO sys.uni_course_keyterms (keyterms, uni_course_id) VALUES ('skilled programmer', 2);
INSERT INTO sys.uni_course_keyterms (keyterms, uni_course_id) VALUES ('creative thinker', 2);
INSERT INTO sys.uni_course_keyterms (keyterms, uni_course_id) VALUES ('problem solving', 2);
INSERT INTO sys.uni_course_keyterms (keyterms, uni_course_id) VALUES ('technical skills', 2);
INSERT INTO sys.uni_course_keyterms (keyterms, uni_course_id) VALUES ('algorithm design', 2);
INSERT INTO sys.uni_course_keyterms (keyterms, uni_course_id) VALUES ('programming', 2);
INSERT INTO sys.uni_course_keyterms (keyterms, uni_course_id) VALUES ('collaborative', 2);
INSERT INTO sys.uni_course_keyterms (keyterms, uni_course_id) VALUES ('project management', 2);

CREATE TABLE sys.uni_application (
  id int PRIMARY KEY auto_increment,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email_address VARCHAR(200) NOT NULL,
  uni_id INT NOT NULL,
  course_id INT NOT NULL,
  first_grade VARCHAR(5) NOT NULL,
  second_grade VARCHAR(5) NOT NULL,
  third_grade VARCHAR(5) NOT NULL,
  other_grade VARCHAR(5),
  grade_score INT NOT NULL,
  personal_statement VARCHAR(4000) NOT NULL,
  ps_score INT NOT NULL,
  total_score INT NOT NULL,
  approved_mkr VARCHAR(1) NOT NULL,
  comments VARCHAR(4000),
  FOREIGN KEY (uni_id) references universities(id),
  FOREIGN KEY (course_id) references courses(id)
);

CREATE TABLE sys.uni_course_keyterms (
  id int PRIMARY KEY auto_increment,
  keyterms varchar(4000) NOT NULL,
  uni_course_id int NOT NULL,
  FOREIGN KEY (uni_course_id) references uni_courses(id)
);
