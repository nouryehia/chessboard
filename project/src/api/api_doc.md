# Doc for API Routes and Usages

## Enrolled_Course
(Prefix = enrolled_course)
### enroll_user
##### Suffix: /enroll_user
##### Request_Type: POST
##### 
Route to enroll a user in to a specific section of a course. 

#### Input:
- user_id : int --> The id of the user to enroll.
- section_id : int --> The section_id of the course to enroll user in.
- course_id : int --> The course_id of the course to enroll user in.
- role (optional) : string --> The role of the enrolled user in the course, default is set to be student. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.


### change_role
##### Suffix: /change_role
##### Request_Type: POST
Route to change the role of an already enrolled user in a specific course.

##### Input:
- user_id : int --> The id of the user to change role.
- course_id : int --> The course_id of the course to change the role of the user in.
- role : string --> The role of the enrolled user in the course. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.


### delete_user_from_course
##### Suffix: /delete_user_from_course
##### Request_Type: POST
HARD delete a user from a course that one enrolled.

##### Input:
- user_id : int --> The id of the user to be deleted.
- course_id : int --> The course_id of the course to delete the user from.

### get_user_of_course
##### Suffix: /get_user_of_course
##### Request_Type: GET
Get the enrolled_course information of a user in a course.

##### Input:
- user_id : int --> The id of the user to be searched.
- course_id : int --> The course_id of the course to be searched.

### get_all_user_in_course
##### Suffix: /get_all_user_in_course
##### Request_Type: GET
Get all the users in a given course (with certain role).

##### Input:
- course_id : int --> The course_id of the course to search for.
- roles : string --> A colon seperated list of strings of all the roles to search for. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.

### get_user_in_section
##### Suffix: /get_user_in_section
##### Request_Type: GET
Get all the users in a given section.

##### Input:
- course_id : int --> The course_id of the course to search for.
- section_id: int --> The section_id of the section to search for.

### get_courses_user_in
##### Suffix: /get_courses_user_in
##### Request_Type: GET
Get all the courses a user is in.

##### Input:
- user_id : int --> The id of the user to saerch for.
- roles : string --> A colon seperated list of strings of all the roles to search for. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.


