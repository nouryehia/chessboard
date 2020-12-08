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

INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('almondaficionados@gmail.com', 'Srayva', 'Balasa', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 0, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('fake@fake.net', 'Yixuan', 'Zhou', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 0, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('fake@fake.gov', 'Bobby', 'Shmurda', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 1, 'false');
INSERT INTO "Users" (email, first_name, last_name, password, urole, request) VALUES ('fake@fake.co.uk', 'Shelly', 'BluGatorade', '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4', 1, 'false');

INSERT INTO "Queue" (status, high_capacity_enable, high_capacity_threshold, high_capacity_message, high_capacity_warning, ticket_cool_down) VALUES (0, true, 10, 'high capacity', 'high capacity', 10);
INSERT INTO "Course" (description, name, quarter, short_name, url, year, active, queue_enabled, cse, lock_button, queue_id, is_deleted, instructor_id) VALUES ('Test Course', 'Test', 0, 'T1', 'wic.ucsd.edu', 2022, true, false, true, true, 1, false, 1);
INSERT INTO "Section" (section_name, section_id, course_id) VALUES ('Test Section', 230, 1);

INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status) VALUES (1, 4, 1, 1, 0);
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status) VALUES (2, 4, 1, 1, 0);
INSERT INTO "EnrolledCourse" (user_id, role, section_id, course_id, status) VALUES (3, 3, 1, 1, 0);