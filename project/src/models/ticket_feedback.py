from __future__ import annotations

from enum import Enum
from ..utils.time import TimeUtil
# from typing import List

from ...setup import db
# from .user import User  # Pretending
# from .queue import Queue
# from .ticket import Ticket, Status
# from typing import List


class Rating(Enum):
    """
    The ratings for the feedback, with the following option --> Database
    value:\n
    BAD --> 0
    NEUTRAL --> 1
    GOOD --> 2
    """
    BAD = 0
    NEUTRAL = 1
    GOOD = 2


class TicketFeedback(db.Model):
    """
    The ticket_feedback model that is in the data base.
    Fields:\n
    id --> The id of the ticket_feedback, unique primary key.\n
    ticket_id --> The id of the ticket that this feedback is associated to.\n
    rating --> The rating to this ticket_feedback.\n
    feedback --> The actual written feedback. Nullable.\n
    submitted_date --> The time that this feedback is submited.\n
    is_annoymous --> Whether this ticket feedback is annoymous.\n
    @author Yixuanzhou
    """
    __tablename__ = 'TicketFeedback'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),
                          nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(255), nullable=True)
    submitted_date = db.Column(db.DateTime, nullable=False,
                               default=TimeUtil.get_current_time())
    is_annoymous = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        """
        The constructor of the ticket object.\n
        Inputs:\n
        ticket_id --> The id of the ticket that this feedback belongs to.\n
        rating --> The rating of the ticket.\n
        feedback --> The actual feedback content.\n
        submitted_date --> The time it is submited.\n
        is_annoymous --> Whether the feedback is left annoymously.\n
        Return:\n
        The created ticket feedback object
        """
        super(TicketFeedback, self).__init__(**kwargs)

    def save(self):
        """
        Save the object to the database.
        """
        db.session.commit()

    # Static add method
    @staticmethod
    def add_to_db(tf: TicketFeedback):
        """
        Add the queue to the database.\n
        Inputs:\n
        tf --> the ticketfeedback object created.\n
        """
        db.session.add(tf)
        db.session.commit()
