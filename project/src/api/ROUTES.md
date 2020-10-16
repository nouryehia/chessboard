# Routes

## ***Notes***

- List any routes you want us to add/change here.
- Also bugs lol but mucho changed recently so a lot of routes are broken rn but they'll be fixed soon

# Doc for API Routes and Usages

## ***Course***
(Prefix = course)
### **create_course (POST)**
#### *Description*
Route to create a course.

#### *Parameters*
- **description: str** --> The description for the course.
- **name: str** --> The name for the course to be created.
- **quarter: str** --> The quarter of the course. Candidates: FALL, WINTER, SPRING, SS1, SS2
- **short_name: str** --> The short name of the course.
- **url: str** --> The url of the course.
- **year: int** --> The year of the course.
- **active: bool** --> Whether the course is active or not.
- **queue_enabled: bool** --> Whether the course has a queue enabled.
- **cse: bool** --> Whether the course is in cse department.
- **queue_id: int** --> The id of the queue belongs to the course.

#### *Responses*
- **{'reason': 'course created'}, 200** if the course is successfully created.
- **{'reason': 'course existed'}, 400** if the course has existed already.

### **delete_course (POST)**
#### *Description*
Route to delete a course.

#### *Parameters*
- **quarter: str** --> The quarter of the course. Candidates: FALL, WINTER, SPRING, SS1, SS2
- **short_name: str** --> The short name of the course.
- **year: int** --> The year of the course.
- **active: bool** --> Whether the course is active or not.

#### *Responses*
- **{'reason': 'course deleted'}, 200** if the course is successfully deleted.
- **{'reason': 'course non-existed'}, 400** if the course was not existed originally.

### **find_course_by_id (GET)**
#### *Description*
Find a course based on its course id.

#### *Parameters*
- **id: str** --> The id of the course to search for.

#### *Responses*
- **{''reason': 'course not found'}, 400** if the course is not found.
- **{'reason': 'course found' 'result': c}, 200** where **c** is
```python
c = {
    'id': 'The id of the course'
    'description': 'The description of the course'
    'name': 'The name of the course'
    'quarter': 'The quarter of the course'
    'url': 'The url of the course'
    'year': 'The year of the course'
    'active': 'bool value indicate whether the course is currently active'
    'queue_enabled': 'bool value indicate whether the course has a queue'
    'cse': 'bool value indicate whether the course belongs to cse'
    'lock_button': 'bool value indicate whether we need a lock button for queue'
    'queue_id': 'The id of the queue'
    'is_deleted': 'Whether the course has been deleted'
}
```

### **find_all_courses (GET)**
#### *Description*
Find all the courses in the database

#### *Parameters*
- **quarter: str** --> Optional parameter for finding courses only in a quarter. When this is specified, the year parameter must also be specified. Candidates: FALL, WINTER, SPRING, SS1, SS2
- **year: int** --> Optional parameter for finding courses only in a designated year.

#### *Responses*
- **{'reason': 'successed', 'result': crs}** where **crs** is 
```python
crs = [{
    'id': 'The id of the course'
    'description': 'The description of the course'
    'name': 'The name of the course'
    'quarter': 'The quarter of the course'
    'url': 'The url of the course'
    'year': 'The year of the course'
    'active': 'bool value indicate whether the course is currently active'
    'queue_enabled': 'bool value indicate whether the course has a queue'
    'cse': 'bool value indicate whether the course belongs to cse'
    'lock_button': 'bool value indicate whether we need a lock button for queue'
    'queue_id': 'The id of the queue'
    'is_deleted': 'Whether the course has been deleted'
}]
```


## ***Enrolled_Course***
(Prefix = enrolled_course)
### **enroll_user (POST)**
#### *Description*
Route to enroll a user in to a specific section of a course. 

#### *Parameters*
- **user_id: int** --> The id of the user to enroll.
- **section_id: int** --> The section_id of the course to enroll user in.
- **course_id: int** --> The course_id of the course to enroll user in.
- **role (optional): string** --> The role of the enrolled user in the course, default is set to be student. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.

#### *Responses*
- **{'reason': 'user enrolled}, 200** when the request success.
- **{'reason': 'user existed}, 400** when the request failed due to a user is already enrolled.


### **change_role (POST)**
#### *Description*
Route to change the role of an already enrolled user in a specific course.

#### *Parameters*
- **user_id: int** --> The id of the user to change role.
- **course_id: int** --> The course_id of the course to change the role of the user in.
- **role: string** --> The role of the enrolled user in the course. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.

#### *Responses*
- **{'reason': 'Role changed'}, 200** when role is successfully changed.
- **{'reason': ' User not enrolled'}, 400** when the user is not enrolled in the course.


### **delete_user_from_course (POST)**
#### *Description*
HARD delete a user from a course that one enrolled.

#### *Parameters*
- **user_id: int** --> The id of the user to be deleted.
- **course_id: int** --> The course_id of the course to delete the user from.

#### *Responses*
- **{'reason': 'user deleted'}, 200** when the user is successfully deleted.
- **{'reason': 'user not found'}, 400** when the user is not found in the course.

### **get_user_of_course (GET) **
#### *Description*
Get the enrolled_course information of a user in a course.

#### *Parameters*
- **user_id: int** --> The id of the user to be searched.
- **course_id: int** --> The course_id of the course to be searched.

#### *Responses*
- **{'reason': 'success', 'result': ret}, 200** where **ret** consists of the following:
```python
ret = {
    'user_info': {
        'fname': 'The first name of the user'
        'lname': 'The last name of the user'
        'email': 'The email of the user'
        'id': 'The id of the user'
        'pid': 'The pid of the user'
        'last_login': 'Time stamp of the last time this user logged in'
    }
    'enrolled_course_info': {
        'user_id': 'The user_id of the enrolled_course entry'
        'course_id': 'The course id of this enrolled_course entry'
        'section_id': 'The section id of this enroleld_course entry'
        'id': 'The id of this enrolled_course entry'
        'status': 'The status of this enrolled_course entry (for tutor avalibilities)'
        'role' : 'The role of this enrolled_course entry'
    }
}
```

### **get_all_user_in_course (GET)**
#### *Description*
Get all the users in a given course (with certain role).

#### *Parameters*
- **course_id: int** --> The course_id of the course to search for.
- **roles: string** --> A colon seperated list of strings of all the roles to search for. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.

#### *Responses*
- **{'reason': 'success', 'result': ret}, 200** where **ret** is
```python
ret = [{
    'user_info': {
        'fname': 'The first name of the user'
        'lname': 'The last name of the user'
        'email': 'The email of the user'
        'id': 'The id of the user'
        'pid': 'The pid of the user'
        'last_login': 'Time stamp of the last time this user logged in'
    }
    'enrolled_user_info': {
        'user_id': 'The user_id of the enrolled_course entry'
        'course_id': 'The course id of this enrolled_course entry'
        'section_id': 'The section id of this enroleld_course entry'
        'id': 'The id of this enrolled_course entry'
        'status': 'The status of this enrolled_course entry (for tutor avalibilities)'
        'role' : 'The role of this enrolled_course entry'
    }
}]
```
- **{'reason': 'course not found'}, 400** when failed.

### **get_user_in_section (GET)**
#### *Description*
Get all the users in a given section.

#### *Parameters*
- **course_id: int** --> The course_id of the course to search for.
- **section_id: int** --> The section_id of the section to search for.

#### *Responses*
- **{'reason': 'success', 'result': ret}, 200** where **ret** is
```python
ret = [{
    'user_info': {
        'fname': 'The first name of the user'
        'lname': 'The last name of the user'
        'email': 'The email of the user'
        'id': 'The id of the user'
        'pid': 'The pid of the user'
        'last_login': 'Time stamp of the last time this user logged in'
    }
    'enrolled_user_info': {
        'user_id': 'The user_id of the enrolled_course entry'
        'course_id': 'The course id of this enrolled_course entry'
        'section_id': 'The section id of this enroleld_course entry'
        'id': 'The id of this enrolled_course entry'
        'status': 'The status of this enrolled_course entry (for tutor avalibilities)'
        'role' : 'The role of this enrolled_course entry'
    }
}]
```


### **get_courses_user_in (GET)**
#### *Description*
Get all the courses a user is in.

#### *Parameters*
- **user_id: int** --> The id of the user to saerch for.
- **roles: string** --> A colon seperated list of strings of all the roles to search for. Candidates: ROOT, ADMIN, INSTRUCTOR, GRADER, STUDENT.

#### *Responses*
- **'reason': 'success', 'result': ret}), 200** where **ret** is
```python
ret = {
    'user_info': {
        'fname': 'The first name of the user'
        'lname': 'The last name of the user'
        'email': 'The email of the user'
        'id': 'The id of the user'
        'pid': 'The pid of the user'
        'last_login': 'Time stamp of the last time this user logged in'
    }
    'courses': [{
        'user_id': 'The user_id of the enrolled_course entry'
        'course_id': 'The course id of this enrolled_course entry'
        'section_id': 'The section id of this enroleld_course entry'
        'id': 'The id of this enrolled_course entry'
        'status': 'The status of this enrolled_course entry (for tutor avalibilities)'
        'role' : 'The role of this enrolled_course entry'
    }]
}
```

### **find_active_tutor_for (GET)**
#### *Description*
Get all the active tutor of a queue.

#### *Parameters*
- **queue_id: int** --> The id of the queue to search for.


## ***Ticket API***

### **add_ticket (POST)**

#### *Description*

Adds a ticket to the queue. 

#### *Parameters*

- **queue_id: int** id of queue ticket is on
- **student_id: int** (DEV ONLY) id of student who added the ticket
- **title: string** title of ticket
- **description: string** description of ticket
- **room: string** room where ticket was added
- **workstation: string** workstation ticket was added on
- **is_private: int** whether the ticket is private. pass in 0 or 1
- **help_type: string** help type. see ../models/ticket.py for help types
- **tag_list: string** list of tags associated with tickets. pass in semi-colon separated list. see ../models/ticket.py for ticket tags

#### *Responses*
- **'reason': 'ticket added to queue', 'result': ret}), 200** where **ret** is
```json
ret = {
    "ticket_events": events attached to this ticket (null if none),
    "ticket_info": {
        "accepted_at": when the ticket was accepted (null if pending),
        "closed_at": when the ticket was closed (null if pending or open),
        "created_at": when the ticketw as created,
        "description": description of ticket,
        "grader_id": id of grader on ticket (null if none),
        "help_type": help type (see ../models/ticket.py),
        "is_private": whether the ticket is private,
        "queue_id": id of queue ticket is on,
        "room": ticket room,
        "status": ticket status (see ../models/ticket.py),
        "student_id": id of student who made the ticket,
        "tag_one": first ticket tag (see ../models/ticket.py),
        "tag_two": second ticket tag (see ../models/ticket.py) (null if none),
        "tag_three": third ticket tag (see ../models/ticket.py) (null if none),
        "ticket_id": ticket id,
        "title": title of ticket,
        "workstation": workstation of ticket
    }
}
```

### **get_info (GET)**

#### *Description*

Get all of a ticket's properties in json format.

#### *Parameters*

- **user_id: int** id of user requesting to view ticket info
- **ticket_id: int** id of ticket

#### *Responses*
```json
{
    "ticket_events": events attached to this ticket (null if none),
    "ticket_info": {
        "accepted_at": when the ticket was accepted (null if pending),
        "closed_at": when the ticket was closed (null if pending or open),
        "created_at": when the ticketw as created,
        "description": description of ticket,
        "grader_id": id of grader on ticket (null if none),
        "help_type": help type (see ../models/ticket.py),
        "is_private": whether the ticket is private,
        "queue_id": id of queue ticket is on,
        "room": ticket room,
        "status": ticket status (see ../models/ticket.py),
        "student_id": enrolled course id of student who made the ticket,
        "tag_one": first ticket tag (see ../models/ticket.py),
        "tag_two": second ticket tag (see ../models/ticket.py) (null if none),
        "tag_three": third ticket tag (see ../models/ticket.py) (null if none),
        "ticket_id": ticket id,
        "title": title of ticket,
        "workstation": workstation of ticket
    }
}
```

### **get_user_permissions (GET)**

#### *Description*

Determines if a user can view or edit a ticket

#### *Parameters*

- **user_id: int** id of user whose permissions are being checked
- **ticket_id: int** id of ticket

#### *Responses*
```json
{
    "can_edit": whether the passed in user can edit the ticket,
    "can_view": whether the passed in user can view the ticket
}
```

### **student_update (POST)**

#### *Description*

Allows students to update tickets

#### *Parameters*

- **ticket_id: int** id ticket to be updated
- **cancel: int** (OPTIONAL) pass in 1 if student is canceling ticket.
- **title: string** (OPTIONAL) new title
- **description: string** (OPTIONAL) new description
- **room: string** (OPTIONAL) new room
- **workstation: string** (OPTIONAL) new workstation
- **help_type: int** (OPTIONAL) new help type
- **is_private: int** (OPTIONAL) new privacy (0 or 1)

#### *Responses*
- Success:
```json
{
    "reason": "ticket updated",
}
```
- No permission:

```json
{
    "reason": "Permission denied",
}
```
- Other error:
```json
{
    "reason": "ticket could not be updated",
}
```

### **grader_update (POST)**

#### *Description*

Allows graders to update tickets and change status

#### *Parameters*

- **ticket_id: int** id ticket to be updated
- **status: string** new status ('RESOLVED', 'CANCELED', or 'DEFERRED')

#### *Responses*
- Success:
```json
{
    "status": new status,
    "grader_name": name of grader,
    "grader_pid": pid of grader
}
```
- No permission:

```json
{
    "reason": "Permission denied",
}
```

### **defer_accepted_tickets_for_grader (POST)**

#### *Description*

Returns tickets accepted by a grader to the queue

#### *Parameters*

- **queue_id: int** id of queue ticket is on

#### *Responses*
```json
{
    "reason": "# tickets deferred", where # is the number of tickets deferred,
}
```

### **find_all_tickets (GET)**

#### *Description*

Route used to find tickets on the queue (can be catgorized as pending or
accepted)

#### *Parameters*

- **queue_id: int** id of queue we want tickets from
- **pending: int** (OPTIONAL) pass in 1 if you only want pending tickets
- **accepted: int** (OPTIONAL) pass in 1 if you only want accepted tickets

#### *Responses*
```json
{
    {
        "ticket_events": events attached to this ticket (null if none),
        "ticket_info": {
            "accepted_at": when the ticket was accepted (null if pending),
            "closed_at": when the ticket was closed (null if pending or open),
            "created_at": when the ticketw as created,
            "description": description of ticket,
            "grader_id": id of grader on ticket (null if none),
            "help_type": help type (see ../models/ticket.py),
            "is_private": whether the ticket is private,
            "queue_id": id of queue ticket is on,
            "room": ticket room,
            "status": ticket status (see ../models/ticket.py),
            "student_id": enrolled course id of student who made the ticket,
            "tag_one": first ticket tag (see ../models/ticket.py),
            "tag_two": second ticket tag (see ../models/ticket.py) (null if none),
            "tag_three": third ticket tag (see ../models/ticket.py) (null if none),
            "ticket_id": ticket id,
            "title": title of ticket,
            "workstation": workstation of ticket
        }
    }
    ...
}
```