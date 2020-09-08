# Routes

## ***Notes***

- List any routes you want us to add/change here.
- Also bugs lol but mucho changed recently so a lot of routes are broken rn but they'll be fixed soon

# Doc for API Routes and Usages

## **Enrolled_Course**
(Prefix = enrolled_course)
### ** enroll_user (POST)**
#### *Description*
Route to enroll a user in to a specific section of a course. 

#### *Parameters*
- user_id : int --> The id of the user to enroll.
- section_id : int --> The section_id of the course to enroll user in.
- course_id : int --> The course_id of the course to enroll user in.
- role (optional) : string --> The role of the enrolled user in the course, default is set to be student. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.


### **change_role* (POST)*
#### *Description*
Route to change the role of an already enrolled user in a specific course.

#### *Parameters*
- user_id : int --> The id of the user to change role.
- course_id : int --> The course_id of the course to change the role of the user in.
- role : string --> The role of the enrolled user in the course. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.


### **delete_user_from_course (POST)**
#### *Description*
HARD delete a user from a course that one enrolled.

#### *Parameters*
- user_id : int --> The id of the user to be deleted.
- course_id : int --> The course_id of the course to delete the user from.

### **get_user_of_course (GET) **
#### *Description*
Get the enrolled_course information of a user in a course.

#### *Parameters*
- user_id : int --> The id of the user to be searched.
- course_id : int --> The course_id of the course to be searched.

### **get_all_user_in_course (GET)**
#### *Description*
Get all the users in a given course (with certain role).

#### *Parameters*
- course_id : int --> The course_id of the course to search for.
- roles : string --> A colon seperated list of strings of all the roles to search for. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.

### **get_user_in_section (GET)**
#### *Description*
Get all the users in a given section.

#### *Parameters*
- course_id : int --> The course_id of the course to search for.
- section_id: int --> The section_id of the section to search for.

### **get_courses_user_in (GET)**
#### *Description*
Get all the courses a user is in.

#### *Parameters*
- user_id : int --> The id of the user to saerch for.
- roles : string --> A colon seperated list of strings of all the roles to search for. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.


### **find_active_tutor_for (GET)**
#### *Description*
Get all the active tutor of a queue.

#### *Parameters*
- queue_id : int --> The id of the queue to search for.


## ***Ticket API***

### **add_ticket (POST)**

#### *Description*

Adds a ticket to the queue. 

#### *Parameters*

- **queue_id:** id of queue ticket is on
- **student_id:** id of student who added the ticket
- **title:** title of ticket
- **description:** description of ticket
- **room:** room where ticket was added
- **workstation:** workstation ticket was added on
- **is_private:** whether the ticket is private. pass in 0 or 1
- **help_type:** help type. see ../models/ticket.py for help types
- **tag_list:** list of tags associated with tickets. pass in semi-colon separated list. see ../models/ticket.py for ticket tags

### **get_info (GET)**

#### *Description*

Get all of a ticket's properties in json format.

#### *Parameters*

- **user_id:** id of user requesting to view ticket info
- **ticket_id:** id of ticket

### **get_user_permissions (GET)**

#### *Description*

Determines if a user can view or edit a ticket

#### *Parameters*

- **user_id:** id of user whose permissions are being checked
- **ticket_id:** id of ticket






