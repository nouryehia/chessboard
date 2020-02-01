DROP DATABASE autograder;
CREATE DATABASE IF NOT EXISTS autograder CHARACTER SET utf8;
USE autograder;

CREATE TABLE `Users` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`email` varchar(255) NOT NULL UNIQUE,
	`first_name` varchar(255) NOT NULL,
	`last_name` varchar(255) NOT NULL,
	`password` varchar(255) NOT NULL,
	`pid` varchar(10) NOT NULL UNIQUE,
	`last_login` DATETIME,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Checkoff` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`description` varchar(255) NOT NULL,
	`name` varchar(255) NOT NULL,
	`suite_id` bigint(20) NOT NULL,
	`points` int(11) NOT NULL DEFAULT '1',
	PRIMARY KEY (`id`)
);

CREATE TABLE `CheckoffSuite` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`status` int(11) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `CheckoffEvaluation` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`checkoff_time` DATETIME NOT NULL,
	`checkoff_id` bigint(20) NOT NULL,
	`grader_id` bigint(20) NOT NULL,
	`student_id` bigint(20) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Queue` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`status` int(11) NOT NULL,
	`high_capacity_enabled` BOOLEAN NOT NULL DEFAULT false,
	`high_capacity_threshold` bigint(20) NOT NULL DEFAULT '25',
	`high_capacity_message` varchar(255) NOT NULL DEFAULT 'The queue is currently at high capacity. The tutors will be limiting their time to 5 minutes per student.',
	`high_capacity_warning` varchar(255) NOT NULL DEFAULT 'The queue is currently very busy. You may not be helped before tutor hours end.',
	`ticket_cool_down` int(11) NOT NULL DEFAULT '10',
	PRIMARY KEY (`id`)
);

CREATE TABLE `Course` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`description` varchar(255),
	`name` varchar(255) NOT NULL,
	`quarter` int(11) NOT NULL,
	`short_name` varchar(255) NOT NULL,
	`url` varchar(255),
	`year` int(11) NOT NULL,
	`active` BOOLEAN NOT NULL,
	`queue_enabled` BOOLEAN NOT NULL,
	`cse` BOOLEAN NOT NULL DEFAULT true,
	`lock_button` BOOLEAN DEFAULT true,
	`queue_id` bigint(20) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `EnrolledCourse` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`user_id` bigint(20) NOT NULL,
	`role` int(11) NOT NULL,
	`section_id` bigint(20) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Section` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`section_name` varchar(255) NOT NULL,
	`section_id` bigint(20) NOT NULL,
	`course_id` bigint(20) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Ticket` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`created_at` DATETIME NOT NULL,
	`closed_at` DATETIME,
	`room` varchar(255),
	`workstation` varchar(255),
	`status` int(11) NOT NULL,
	`title` varchar(255) NOT NULL,
	`description` longtext NOT NULL,
	`grader_id` bigint(20),
	`queue_id` bigint(20) NOT NULL,
	`student_id` bigint(20) NOT NULL,
	`is_private` BOOLEAN NOT NULL DEFAULT false,
	`accepted_at` DATETIME,
	`help_type` int(11) NOT NULL,
	`tag_one` int(11) NOT NULL,
	`tag_two` int(11),
	`tag_three` int(11),
	PRIMARY KEY (`id`)
);

CREATE TABLE `TicketFeedback` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`ticket_id` bigint(20) NOT NULL,
	`rating` int(11) NOT NULL,
	`feedback` longtext,
	`submitted_date` DATETIME NOT NULL,
	`is_anonymous` BOOLEAN NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `TicketEvent` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`type` int(11) NOT NULL,
	`ticket_id` bigint(20) NOT NULL,
	`message` varchar(255) NOT NULL,
	`is_anonymous` BINARY NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `QueueLoginEvent` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`event_type` int(11) NOT NULL,
	`action_type` int(11) NOT NULL,
	`timestamp` DATETIME NOT NULL,
	`tutor_id` bigint(20) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `NewsFeedPost` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`created_at` DATETIME NOT NULL,
	`is_deleted` BOOLEAN NOT NULL,
	`last_edited_at` DATETIME,
	`subject` varchar(255) NOT NULL,
	`body` longtext NOT NULL,
	`owner_id` bigint(20) NOT NULL,
	`queue_id` bigint(20) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Assignment` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`due` DATETIME NOT NULL,
	`is_deleted` BOOLEAN NOT NULL,
	`name` varchar(255) NOT NULL,
	`category_id` bigint(20) NOT NULL,
	`checkoff_suite_id` bigint(20) NOT NULL,
	`total_grade_percent` double NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Category` (
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL,
	`weight` double NOT NULL,
	`course_id` bigint(20) NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `Checkoff` ADD CONSTRAINT `Checkoff_fk0` FOREIGN KEY (`suite_id`) REFERENCES `CheckoffSuite`(`id`);

ALTER TABLE `CheckoffEvaluation` ADD CONSTRAINT `CheckoffEvaluation_fk0` FOREIGN KEY (`checkoff_id`) REFERENCES `Checkoff`(`id`);

ALTER TABLE `CheckoffEvaluation` ADD CONSTRAINT `CheckoffEvaluation_fk1` FOREIGN KEY (`grader_id`) REFERENCES `Users`(`id`);

ALTER TABLE `CheckoffEvaluation` ADD CONSTRAINT `CheckoffEvaluation_fk2` FOREIGN KEY (`student_id`) REFERENCES `Users`(`id`);

ALTER TABLE `Course` ADD CONSTRAINT `Course_fk0` FOREIGN KEY (`queue_id`) REFERENCES `Queue`(`id`);

ALTER TABLE `EnrolledCourse` ADD CONSTRAINT `EnrolledCourse_fk0` FOREIGN KEY (`user_id`) REFERENCES `Users`(`id`);

ALTER TABLE `EnrolledCourse` ADD CONSTRAINT `EnrolledCourse_fk1` FOREIGN KEY (`section_id`) REFERENCES `Section`(`id`);

ALTER TABLE `Section` ADD CONSTRAINT `Section_fk0` FOREIGN KEY (`course_id`) REFERENCES `Course`(`id`);

ALTER TABLE `Ticket` ADD CONSTRAINT `Ticket_fk0` FOREIGN KEY (`grader_id`) REFERENCES `EnrolledCourse`(`user_id`);

ALTER TABLE `Ticket` ADD CONSTRAINT `Ticket_fk1` FOREIGN KEY (`queue_id`) REFERENCES `Queue`(`id`);

ALTER TABLE `Ticket` ADD CONSTRAINT `Ticket_fk2` FOREIGN KEY (`student_id`) REFERENCES `EnrolledCourse`(`user_id`);

ALTER TABLE `TicketFeedback` ADD CONSTRAINT `TicketFeedback_fk0` FOREIGN KEY (`ticket_id`) REFERENCES `Ticket`(`id`);

ALTER TABLE `TicketEvent` ADD CONSTRAINT `TicketEvent_fk0` FOREIGN KEY (`ticket_id`) REFERENCES `Ticket`(`id`);

ALTER TABLE `QueueLoginEvent` ADD CONSTRAINT `QueueLoginEvent_fk0` FOREIGN KEY (`tutor_id`) REFERENCES `Users`(`id`);

ALTER TABLE `NewsFeedPost` ADD CONSTRAINT `NewsFeedPost_fk0` FOREIGN KEY (`owner_id`) REFERENCES `EnrolledCourse`(`id`);

ALTER TABLE `NewsFeedPost` ADD CONSTRAINT `NewsFeedPost_fk1` FOREIGN KEY (`queue_id`) REFERENCES `Queue`(`id`);

ALTER TABLE `Assignment` ADD CONSTRAINT `Assignment_fk0` FOREIGN KEY (`category_id`) REFERENCES `Category`(`id`);

ALTER TABLE `Assignment` ADD CONSTRAINT `Assignment_fk1` FOREIGN KEY (`checkoff_suite_id`) REFERENCES `CheckoffSuite`(`id`);

ALTER TABLE `Category` ADD CONSTRAINT `Category_fk0` FOREIGN KEY (`course_id`) REFERENCES `Course`(`id`);

