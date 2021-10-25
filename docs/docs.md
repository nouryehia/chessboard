---
layout: default
---

# Backend Documentation
In this file, we dive deeper into the details of the application.

## Application
The application is separated into two parts, with `models` directory containing 
all the database models that are used to communicate with the database, and `apis`
storing the `api` routes that we expose to the frontend to fulfill functionalities. 
In the following [Model](#Models) section, we go detail in most of the models that
we have to describe its purpose and functionalities, and in the [Apis](#Apis) section
we list the ports that we exposed and their functionalities. 

### Models

#### user
The application starts with the `user` model which is used to register users with
their login credentials, user info, and the role of the user within the app.
Every other models that interact with any user will use the uniquely identifiable
key of user, its `id` field, to reference it.


#### course
Another backbone component is the `course` model, which also holds the queue. 

#### enrolled_course
`enrolled_course` model is very important because it is used to associate users
with courses. Because in SQL we cannot store a list as an entry of a table, we thus
use another table/database model to contain the associate of users and courses.
And entry of `enrolled_course` contains `user_id` and `course_id` and `section_id`, 
which indicates a user is associate with a course/section. It also specifies the
role of the user within the course, so we can separate users into instructors, 
tutors and students, and thus grant them different permissions. 

### Apis

## Testing




---
[go back](/chessboard)