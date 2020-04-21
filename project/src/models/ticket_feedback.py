from __future__ import annotations

from enum import Enum
from ..utils.time import TimeUtil
from typing import List

from ...setup import db
from .model.user import User  # Pretending
from .model.queue import Queue
from .model.ticket import Ticket, Status


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
    submitted_date = db.Column(db.Datetime, nullable=False,
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

    # Static query methods for ticket feedbacks
    @staticmethod
    def get_ticket_feedback(ticket_list: List[Ticket]) -> List[TicketFeedback]:
        """
        Given a list of tickets, get the feedback of each ticket and put
        them into a list.\n
        Inputs:\n
        ticket_list --> The list of tickets to look for.\n
        Returns:\n
        A list of TicketFeedback, if a ticket does not have a feedback,
        it will not show up in the list.\n
        """
        feedback_list = []
        for ticket in ticket_list:
            feedback = TicketFeedback.query().filter_by(ticket_id=ticket.id)\
                        .ordered_by(TicketFeedback.submitted_date).first()
            if feedback is not None:
                feedback_list.append(feedback)
        return feedback_list

    @staticmethod
    def find_all_feedback_for_queue(queue: Queue):
        """
        Find all the feedback of the tickets in a queue.\n
        Inputs:\n
        queue --> The Queue object to search for.\n
        Return:\n
        A list of feedbacks of this queue.\n
        """
        tickets = Ticket.find_all_tickets(queue, [Status.RESOLVED])
        return Ticket.get_ticket_feedback(tickets)

    @staticmethod
    def find_for_grader(queue: Queue, grader: User) -> List[TicketFeedback]:
        """
        Find all the feedback to a grader that is in the queue.
        Inputs:\n
        queue --> The Queue object to search for.\n
        grader --> The User object for the grader to search for.\n
        Return:\n
        A list of ticket feedbacks to the grader.\n
        """
        tickets = Ticket.find_all_tickets_for_grader(queue, grader)
        return TicketFeedback.get_ticket_feedback(tickets)

    @staticmethod
    def find_for_student(queue: Queue, student: User) -> List[TicketFeedback]:
        """
        Find all the feedback from a student that is in the queue.
        Inputs:\n
        queue --> The Queue object to search for.\n
        student --> The User object for the student to search for.\n
        Return:\n
        A list of ticket feedbacks from the student.\n
        """
        tickets = Ticket.find_all_tickets_for_student(queue, student)
        return TicketFeedback.get_ticket_feedback(tickets)
