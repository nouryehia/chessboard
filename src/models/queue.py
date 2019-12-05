from app import db
from enum import Enum
from user import User
from ticket import Ticket, HelpType, TicketTag,\
                   find_pending_ticket_by_student,\
                   student_update
from typing import List


"""
Define Constant
"""
MILLIS_MINUTE_CONVERT = 60 * 1000
DEFAULT_WAIT_TIME = 12 * 60 * 1000  # 12min
MIN_WAIT_TIME = 5 * 60 * 1000  # 5min


class Status(Enum):
    """
    The status of the queue with the following options --> database value:\n
    OPEN --> 0\n
    LOCKED --> 1\n
    CLOSED --> 2\n
    """
    OPEN = 0
    LOCKED = 1
    CLOSED = 2


class Queue(db.Model):
    """
    The main queue handler for the queue page.\n
    Fields: \n
    id --> The id of the queue, unique primary key.\n
    status --> The status of the queue, not nullable.\n
    highCapacityEnabled --> Boolean if the high capacity is on, not nullable.\n
    highCapacityThreshold --> The threshold to identiify if the queue is\
                            at high capacity, not nullable.\n
    highCapacityMessage --> The message to show when high capcity for tutors.\n
    highCapacityWarning --> The warning message to show when\
                            high capacity for students.\n
    defaultTagsEnabled --> If the tag of the queue is enabled. ??? \n
    ticketCooldown --> Int for the time to wait between two tickets
                       submisions.\n
    """
    __tablename__ = 'Queue'
    id = db.Column(db.Integer(20), primary_key=True, nullable=False)
    status = db.Column(db.Integer(11), nullable=False)
    high_capacity_enabled = db.Column(db.Boolean, nullable=False, default=True)
    high_capacity_threshold = db.Column(db.Integer(20), nullable=False,
                                        default=25)
    high_capacity_message = db.Column(db.Text, nullable=False,
                                      default='The queue is currently at high \
                                               capacity. The tutors will be \
                                               limiting their time to 5\
                                               minutes per student.')
    high_capacity_warning = db.Column(db.Text, nullable=False,
                                      default='The queue is currently very busy. \
                                              You may not be helped before \
                                              tutor hours end.')
    ticket_cooldown = db.Column(db.Integer(11), nullable=False, default=10)

    def add_or_update_ticket(self, student: User, title: str,
                             description: str, room: str, workstation: str,
                             is_private: bool, help_type: HelpType,
                             tag_list: List[TicketTag]) -> Ticket:
        old_ticket = find_pending_ticket_by_student(queue=self, 
                                                    student=student)
        if (old_ticket is not None):
            old_ticket.student_update(title=title, description=description,
                                      room=room, workstation=workstation, 
                                      is_private=is_private, 
                                      help_type=help_type,
                                      tag_list=tag_list)
