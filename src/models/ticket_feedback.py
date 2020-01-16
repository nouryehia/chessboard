from app import db
from enum import Enum
from datetime import datetime


class rating(Enum):
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
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),
                          nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(255), nullable=True)
    submitted_date = db.Column(db.Datetime, nullable=False,
                               default=datetime.now)
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
        db.session.add(self)
        db.session.commit()
