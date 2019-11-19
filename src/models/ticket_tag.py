from app import db
from enum import Enum


class Types (Enum):
    """
    All the types of the tags of a ticket ticket the \
        following options --> database value:
    GETTING_STARTED --> 0\n
    SPECIFICATION --> 1\n
    ALGORITHM --> 2\n
    PROGRAMING_LANGUAGE --> 3\n
    IMPLEMENTATION --> 4\n
    COMPILE_ERROR --> 5\n
    RUNTIME_ERROR --> 6\n
    WRONG_OUTPUT --> 7\n
    INFINITE_LOOP --> 8\n
    WEIRD_BEHAVIOR --> 9\n
    WEIRD_DEBUG --> 10\n
    """
    GETTING_STARTED = 0
    SPECIFICATION = 1
    ALGORITHM = 2
    PROGRAMING_LANGUAGE = 3
    IMPLEMENTATION = 4
    COMPILE_ERROR = 5
    RUNTIME_ERROR = 6
    WRONG_OUTPUT = 7
    INFINITE_LOOP = 8
    WEIRD_BEHAVIOR = 9
    WEIRD_DEBUG = 10

   
class ticket_tag(db.Modle):
    """
    The ticket_tag that stores all the possible tags for a ticket.\n
    Fields:
    id --> The id of the ticket, primary key, auto increment.\ns
    type --> The type of the tag.\n
    ticket_id --> The forien key to which a 
    """
