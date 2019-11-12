from app import db
from enum import Enum


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
    highCapacityEnabled = db.Column(db.Boolean, nullable=False, default=True)
    highCapacityThreshold = db.Column(db.Integer(20), nullable=False,
                                      default=25)
    highCapacityMessage = db.Column(db.Text, nullable=False,
                                    default='The queue is currently at high \
                                            capacity. The tutors will be \
                                            limiting their time to 5 minutes \
                                            per student.')
    highCapacityWarning = db.Column(db.Text, nullable=False,
                                    default='The queue is currently very busy. \
                                             You may not be helped before \
                                             tutor hours end.')
    ticketCooldown = db.Column(db.Integer(11), nullable=False, default=10)
