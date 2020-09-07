# Routes

## ***Notes***

- List any routes you want us to add/change here.
- Also bugs lol but mucho changed recently so a lot of routes are broken rn but they'll be fixed soon


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






