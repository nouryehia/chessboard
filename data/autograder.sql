CREATE TABLE "Users" (
	"id" serial NOT NULL,
	"email" varchar(255) NOT NULL UNIQUE,
	"first_name" varchar(255) NOT NULL,
	"last_name" varchar(255) NOT NULL,
	"password" varchar(255) NOT NULL,
	"pid" varchar(10) UNIQUE,
	"last_login" TIMESTAMP,
	"urole" integer NOT NULL DEFAULT '2',
	"request" BOOLEAN NOT NULL DEFAULT 'false',
	"token" varchar(255) NOT NULL DEFAULT '',
	CONSTRAINT "Users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Checkoff" (
	"id" serial NOT NULL,
	"due" TIMESTAMP NOT NULL, 
	"description" varchar(255) NOT NULL,
	"name" varchar(255) NOT NULL,
	"course_id" bigserial NOT NULL,
	"points" integer NOT NULL DEFAULT '1',
	"status" integer NOT NULL,
	"is_deleted" BOOLEAN NOT NULL,
	CONSTRAINT "Checkoff_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);


CREATE TABLE "CheckoffEvaluation" (
	"id" serial NOT NULL,
	"checkoff_time" TIMESTAMP NOT NULL,
	"checkoff_id" bigserial NOT NULL,
	"grader_id" bigserial NOT NULL,
	"student_id" bigserial NOT NULL,
	"score" integer NOT NULL,
	CONSTRAINT "CheckoffEvaluation_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);


CREATE TABLE "Course" (
	"id" serial NOT NULL,
	"description" varchar(255),
	"name" varchar(255) NOT NULL,
	"quarter" integer NOT NULL,
	"short_name" varchar(255) NOT NULL,
	"url" varchar(255),
	"year" integer NOT NULL,
	"active" BOOLEAN NOT NULL,
	"queue_enabled" BOOLEAN NOT NULL,
	"cse" BOOLEAN NOT NULL DEFAULT 'true',
	"lock_button" BOOLEAN DEFAULT 'true',
	"queue_id" bigserial NOT NULL,
	"is_deleted" BOOLEAN NOT NULL DEFAULT 'false',
	"instructor_id" integer NOT NULL,
	CONSTRAINT "Course_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Queue" (
	"id" serial NOT NULL,
	"status" integer NOT NULL,
	"high_capacity_enable" BOOLEAN NOT NULL DEFAULT 'false',
	"high_capacity_threshold" integer NOT NULL DEFAULT '25',
	"high_capacity_message" varchar(255) NOT NULL,
	"high_capacity_warning" varchar(255) NOT NULL,
	"ticket_cool_down" integer NOT NULL DEFAULT '10',
	"queue_lock" BOOLEAN NOT NULL DEFAULT 'true',
	CONSTRAINT "Queue_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Ticket" (
	"id" serial NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"closed_at" TIMESTAMP,
	"room" varchar(255),
	"workstation" varchar(255),
	"status" integer NOT NULL,
	"title" varchar(255) NOT NULL,
	"description" TEXT NOT NULL,
	"ec_grader_id" bigint,
	"queue_id" bigserial NOT NULL,
	"ec_student_id" bigserial NOT NULL,
	"is_private" BOOLEAN NOT NULL DEFAULT 'false',
	"accepted_at" TIMESTAMP,
	"help_type" integer NOT NULL,
	"tag_one" integer NOT NULL,
	"tag_two" integer,
	"tag_three" integer,
	CONSTRAINT "Ticket_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "EnrolledCourse" (
	"id" serial NOT NULL,
	"user_id" bigserial NOT NULL,
	"role" integer NOT NULL,
	"section_id" bigserial NOT NULL,
	"status" integer NOT NULL,
	"course_id" bigserial NOT NULL,
	"course_short_name" varchar(255) NOT NULL,
	CONSTRAINT "EnrolledCourse_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Section" (
	"id" serial NOT NULL,
	"section_name" varchar(255) NOT NULL,
	"section_id" bigserial NOT NULL UNIQUE,
	"course_id" bigserial NOT NULL,
	CONSTRAINT "Section_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "QueueLoginEvent" (
	"id" serial NOT NULL,
	"event_type" integer NOT NULL,
	"action_type" integer NOT NULL,
	"timestamp" TIMESTAMP NOT NULL,
	"grader_id" bigserial NOT NULL,
	"queue_id"  bigserial NOT NULL,
	CONSTRAINT "QueueLoginEvent_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "TicketEvent" (
	"id" serial NOT NULL,
	"event_type" integer NOT NULL,
	"ticket_id" bigserial NOT NULL,
	"message" varchar(255) NOT NULL,
	"is_private" BOOLEAN NOT NULL,
	"ec_user_id" bigserial NOT NULL,
	"timestamp" TIMESTAMP NOT NULL,
	CONSTRAINT "TicketEvent_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "QueueCalendar" (
	"id" serial NOT NULL,
	"url" TEXT NOT NULL,
	"color" TEXT NOT NULL,
	"is_enabled" BOOLEAN NOT NULL,
	"queue_id" bigserial NOT NULL,
	CONSTRAINT "QueueCalendar_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "NewsFeedPost" (
	"id" serial NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"is_deleted" BOOLEAN NOT NULL,
	"last_edited_at" TIMESTAMP,
	"subject" varchar(255) NOT NULL,
	"body" TEXT NOT NULL,
	"owner_id" bigserial NOT NULL,
	"queue_id" bigserial NOT NULL,
	CONSTRAINT "NewsFeedPost_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "TicketFeedback" (
	"id" serial NOT NULL,
	"ticket_id" bigserial NOT NULL,
	"rating" integer NOT NULL,
	"feedback" TEXT,
	"submitted_date" TIMESTAMP NOT NULL,
	"is_anonymous" BOOLEAN NOT NULL,
	CONSTRAINT "TicketFeedback_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



/*******************************************************************
Autograder stuff
*******************************************************************/

CREATE TABLE "SeatingLayouts" (
	"id" serial NOT NULL,
	"location" varchar(255) NOT NULL,
	"seats" TEXT,
	"count" integer,
	CONSTRAINT "SeatingLayouts_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "AssignedSeats" (
	"id" serial NOT NULL,
	"assignment_name" varchar(255) NOT NULL UNIQUE,
	"layout_id" bigserial NOT NULL,
	"section_id" bigserial NOT NULL,
	"course_id" bigserial NOT NULL,
	"seat_assignments" TEXT,
	CONSTRAINT "AssignedSeats_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "Checkoff" ADD CONSTRAINT "Checkoff_fk0" FOREIGN KEY ("course_id") REFERENCES "Course"("id");


ALTER TABLE "CheckoffEvaluation" ADD CONSTRAINT "CheckoffEvaluation_fk0" FOREIGN KEY ("checkoff_id") REFERENCES "Checkoff"("id");
ALTER TABLE "CheckoffEvaluation" ADD CONSTRAINT "CheckoffEvaluation_fk1" FOREIGN KEY ("grader_id") REFERENCES "Users"("id");
ALTER TABLE "CheckoffEvaluation" ADD CONSTRAINT "CheckoffEvaluation_fk2" FOREIGN KEY ("student_id") REFERENCES "Users"("id");


ALTER TABLE "Course" ADD CONSTRAINT "Course_fk0" FOREIGN KEY ("queue_id") REFERENCES "Queue"("id");
ALTER TABLE "Course" ADD CONSTRAINT "Course_fk1" FOREIGN KEY ("instructor_id") REFERENCES "Users"("id");

ALTER TABLE "Ticket" ADD CONSTRAINT "Ticket_fk0" FOREIGN KEY ("ec_grader_id") REFERENCES "EnrolledCourse"("id");
ALTER TABLE "Ticket" ADD CONSTRAINT "Ticket_fk1" FOREIGN KEY ("queue_id") REFERENCES "Queue"("id");
ALTER TABLE "Ticket" ADD CONSTRAINT "Ticket_fk2" FOREIGN KEY ("ec_student_id") REFERENCES "EnrolledCourse"("id");

ALTER TABLE "EnrolledCourse" ADD CONSTRAINT "EnrolledCourse_fk0" FOREIGN KEY ("user_id") REFERENCES "Users"("id");
ALTER TABLE "EnrolledCourse" ADD CONSTRAINT "EnrolledCourse_fk1" FOREIGN KEY ("section_id") REFERENCES "Section"("id");
ALTER TABLE "EnrolledCourse" ADD CONSTRAINT "EnrolledCourse_fk2" FOREIGN KEY ("course_id") REFERENCES "Course"("id");

ALTER TABLE "Section" ADD CONSTRAINT "Section_fk0" FOREIGN KEY ("course_id") REFERENCES "Course"("id");

ALTER TABLE "QueueLoginEvent" ADD CONSTRAINT "QueueLoginEvent_fk0" FOREIGN KEY ("grader_id") REFERENCES "Users"("id");
ALTER TABLE "QueueLoginEvent" ADD CONSTRAINT "QueueLoginEvent_fk1" FOREIGN KEY ("queue_id") REFERENCES "Queue"("id");

ALTER TABLE "TicketEvent" ADD CONSTRAINT "TicketEvent_fk0" FOREIGN KEY ("ticket_id") REFERENCES "Ticket"("id");
ALTER TABLE "TicketEvent" ADD CONSTRAINT "TicketEvent_fk1" FOREIGN KEY ("ec_user_id") REFERENCES "EnrolledCourse"("id");

ALTER TABLE "QueueCalendar" ADD CONSTRAINT "QueueCalendar_fk0" FOREIGN KEY ("queue_id") REFERENCES "Queue"("id");

ALTER TABLE "NewsFeedPost" ADD CONSTRAINT "NewsFeedPost_fk0" FOREIGN KEY ("owner_id") REFERENCES "EnrolledCourse"("id");
ALTER TABLE "NewsFeedPost" ADD CONSTRAINT "NewsFeedPost_fk1" FOREIGN KEY ("queue_id") REFERENCES "Queue"("id");

ALTER TABLE "TicketFeedback" ADD CONSTRAINT "TicketFeedback_fk0" FOREIGN KEY ("ticket_id") REFERENCES "Ticket"("id");

ALTER TABLE "AssignedSeats" ADD CONSTRAINT "AssignedSeats_fk0" FOREIGN KEY ("layout_id") REFERENCES "SeatingLayouts"("id");
ALTER TABLE "AssignedSeats" ADD CONSTRAINT "AssignedSeats_fk1" FOREIGN KEY ("section_id") REFERENCES "Section"("id");
ALTER TABLE "AssignedSeats" ADD CONSTRAINT "AssignedSeats_fk2" FOREIGN KEY ("course_id") REFERENCES "Course"("id");

INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('almondaficionados@gmail.com', 'Srayva', 'Balasa', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 0, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('fake@fake.net', 'Yixuan', 'Zhou', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 0, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('fake@fake.gov', 'Bobby', 'Shmurda', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 1, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('fake@fake.co.uk', 'Shelly', 'BluGatorade', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 1, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('student@gmail.com', 'A', 'A', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 2, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('tutor@gmail.com', 'B', 'B', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 2, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('lead@gmail.com', 'C', 'C', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 1, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('prof@gmail.com', 'D', 'D', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 0, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('tutorandstudent@gmail.com', 'E', 'E', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 2, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('leadandstudent@gmail.com', 'F', 'F', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 1, 'false');

/* Make 2 test courses */
INSERT INTO "Queue" (status, high_capacity_enable, high_capacity_threshold, high_capacity_message, high_capacity_warning, ticket_cool_down) VALUES (0, true, 10, 'high capacity', 'high capacity', 10);
INSERT INTO "Course" (description, name, quarter, short_name, url, year, active, queue_enabled, cse, lock_button, queue_id, is_deleted, instructor_id) VALUES ('Test Course', 'Test', 0, 'CSE 12', 'wic.ucsd.edu', 2022, true, false, true, true, 1, false, 1);
INSERT INTO "Section" (section_name, section_id, course_id) VALUES ('Test Section', 230, 1);
INSERT INTO "Queue" (status, high_capacity_enable, high_capacity_threshold, high_capacity_message, high_capacity_warning, ticket_cool_down) VALUES (0, true, 10, 'high capacity', 'high capacity', 10);
INSERT INTO "Course" (description, name, quarter, short_name, url, year, active, queue_enabled, cse, lock_button, queue_id, is_deleted, instructor_id) VALUES ('Test Course 2', 'Test2', 0, 'CSE 30', 'wic.ucsd.edu2', 2022, true, false, true, true, 2, false, 1);
INSERT INTO "Section" (section_name, section_id, course_id) VALUES ('Test Section 2', 231, 2);
INSERT INTO "Queue" (status, high_capacity_enable, high_capacity_threshold, high_capacity_message, high_capacity_warning, ticket_cool_down) VALUES (0, true, 10, 'high capacity', 'high capacity', 10);
INSERT INTO "Course" (description, name, quarter, short_name, url, year, active, queue_enabled, cse, lock_button, queue_id, is_deleted, instructor_id) VALUES ('Test Course 3', 'Test3', 0, 'CSE 100', 'wic.ucsd.edu3', 2022, true, false, true, true, 3, false, 1);
INSERT INTO "Section" (section_name, section_id, course_id) VALUES ('Test Section 3', 232, 3);

/* Enroll first 3 users in course 1 and 2nd user in course 2. 4th user is not enrolled in any courses */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (1, 4, 1, 1, 0, 'CSE 12'); /* student */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (2, 1, 1, 1, 0, 'CSE 12'); /* admin */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (3, 3, 1, 1, 0, 'CSE 12'); 
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (2, 3, 2, 2, 0, 'CSE 30'); /* grader */

INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (5, 4, 1, 1, 0, 'CSE 12'); /* student */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (5, 4, 2, 2, 0, 'CSE 30'); /* student */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (6, 3, 1, 1, 0, 'CSE 12'); /* tutor */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (7, 2, 1, 1, 0, 'CSE 12'); /* lead */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (8, 1, 1, 1, 0, 'CSE 12'); /* prof */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (8, 1, 2, 2, 0, 'CSE 30'); /* prof */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (9, 4, 1, 1, 0, 'CSE 12'); /* tutorandstudent */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (9, 4, 2, 2, 0, 'CSE 30'); /* tutorandstudent */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (9, 3, 3, 3, 0, 'CSE 100'); /* tutorandstudent */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (10, 4, 1, 1, 0, 'CSE 12'); /* leadandstudent */
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status, course_short_name) VALUES (10, 2, 3, 3, 0, 'CSE 100'); /* leadandstudent */

/* Create an indexing for the ticket to speed up the query to active tickets */
CREATE INDEX "idx_ticket_isactive" ON "Ticket" USING btree ("status");

INSERT INTO "SeatingLayouts" (location, seats, count) VALUES ('DemoLayout', '[[{"label":"","error":false},{"label":"","error":false},{"label":"F6","left":false,"broken":false,"error":false},{"label":"F5","left":false,"broken":false,"error":false},{"label":"F4","left":true,"broken":false,"error":false},{"label":"","error":false},{"label":"F3","left":false,"broken":false,"error":false},{"label":"F2","left":false,"broken":false,"error":false},{"label":"F1","left":true,"broken":false,"error":false},{"label":"","error":false},{"label":"","error":false}],[{"label":"","error":false},{"label":"E8","left":false,"broken":false,"error":false},{"label":"E7","left":false,"broken":false,"error":false},{"label":"E6","left":false,"broken":true,"error":false},{"label":"E5","left":true,"broken":false,"error":false},{"label":"","error":false},{"label":"E4","left":false,"broken":false,"error":false},{"label":"E3","left":false,"broken":false,"error":false},{"label":"E2","left":false,"broken":false,"error":false},{"label":"E1","left":true,"broken":false,"error":false},{"label":"","error":false}],[{"label":"","error":false},{"label":"D8","left":false,"broken":false,"error":false},{"label":"D7","left":false,"broken":false,"error":false},{"label":"D6","left":false,"broken":false,"error":false},{"label":"D5","left":true,"broken":false,"error":false},{"label":"","error":false},{"label":"D4","left":false,"broken":false,"error":false},{"label":"D3","left":false,"broken":false,"error":false},{"label":"D2","left":false,"broken":false,"error":false},{"label":"D1","left":true,"broken":false,"error":false},{"label":"","error":false}],[{"label":"C10","left":false,"broken":false,"error":false},{"label":"C9","left":false,"broken":false,"error":false},{"label":"C8","left":false,"broken":false,"error":false},{"label":"C7","left":false,"broken":false,"error":false},{"label":"C6","left":true,"broken":false,"error":false},{"label":"","error":false},{"label":"C5","left":false,"broken":false,"error":false},{"label":"C4","left":false,"broken":false,"error":false},{"label":"C3","left":false,"broken":false,"error":false},{"label":"C2","left":false,"broken":false,"error":false},{"label":"C1","left":true,"broken":false,"error":false}],[{"label":"B10","left":false,"broken":false,"error":false},{"label":"B9","left":false,"broken":true,"error":false},{"label":"B8","left":false,"broken":false,"error":false},{"label":"B7","left":false,"broken":false,"error":false},{"label":"B6","left":true,"broken":false,"error":false},{"label":"","error":false},{"label":"B5","left":false,"broken":false,"error":false},{"label":"B4","left":false,"broken":false,"error":false},{"label":"B3","left":false,"broken":false,"error":false},{"label":"B2","left":false,"broken":false,"error":false},{"label":"B1","left":true,"broken":true,"error":false}],[{"label":"","error":false},{"label":"","error":false},{"label":"","error":false},{"label":"","error":false},{"label":"","error":false},{"label":"","error":false},{"label":"","error":false},{"label":"","error":false},{"label":"","error":false},{"label":"","error":false},{"label":"","error":false}],[{"label":"","error":false},{"label":"","error":false},{"label":"A6","left":false,"broken":false,"error":false},{"label":"A5","left":false,"broken":false,"error":false},{"label":"A4","left":true,"broken":false,"error":false},{"label":"","error":false},{"label":"A3","left":false,"broken":false,"error":false},{"label":"A2","left":false,"broken":false,"error":false},{"label":"A1","left":true,"broken":false,"error":false},{"label":"","error":false},{"label":"","error":false}]]', 48);
/* Just a dummy entry for now until the way we save seat assignments is settled */
INSERT INTO "AssignedSeats" (assignment_name, layout_id, section_id, course_id, seat_assignments) VALUES ('Test2 Final', 1, 2, 2, '{"F3":{"name":"24, Student","pid":"A15637"},"F2":{"name":"21, Student","pid":"A15634"},"F1":{"name":"5, Student","pid":"A15618"},"F6":{"name":"0, Student","pid":"A15613"},"F5":{"name":"27, Student","pid":"A15640"},"F4":{"name":"3, Student","pid":"A15616"},"E4":{"name":"6, Student","pid":"A15619"},"E3":{"name":"19, Student","pid":"A15632"},"E2":{"name":"25, Student","pid":"A15638"},"E1":{"name":"8, Student","pid":"A15621"},"E8":{"name":"20, Student","pid":"A15633"},"E7":{"name":"11, Student","pid":"A15624"},"E5":{"name":"1, Student","pid":"A15614"},"D4":{"name":"9, Student","pid":"A15622"},"D3":{"name":"30, Student","pid":"A15643"},"D2":{"name":"26, Student","pid":"A15639"},"D1":{"name":"29, Student","pid":"A15642"},"D8":{"name":"16, Student","pid":"A15629"},"D7":{"name":"31, Student","pid":"A15644"},"D6":{"name":"17, Student","pid":"A15630"},"D5":{"name":"10, Student","pid":"A15623"},"C5":{"name":"14, Student","pid":"A15627"},"C3":{"name":"23, Student","pid":"A15636"},"C1":{"name":"32, Student","pid":"A15645"},"C10":{"name":"2, Student","pid":"A15615"},"C8":{"name":"22, Student","pid":"A15635"},"C6":{"name":"33, Student","pid":"A15646"},"B5":{"name":"7, Student","pid":"A15620"},"B3":{"name":"4, Student","pid":"A15617"},"B10":{"name":"18, Student","pid":"A15631"},"B8":{"name":"15, Student","pid":"A15628"},"B6":{"name":"12, Student","pid":"A15625"},"A3":{"name":"34, Student","pid":"A15647"},"A1":{"name":"13, Student","pid":"A15626"},"A6":{"name":"28, Student","pid":"A15641"}}');