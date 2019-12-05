from app import db
from enum import Enum
from datetime import datetime
from user import User
from ticket import Ticket
from typing import List
from course improt Course # pretending


class EventType(Enum):
    """
    All the event that can happen to a ticket with the \
        following options --> database value:\n
    CREATED --> 0
    ACCEPTED --> 1
    RESOLVED --> 2
    UPDATED --> 3
    DEFERED --> 4
    CANCELED --> 5
    COMMENTED --> 6
    """
    CREATED = 0
    ACCEPTED = 1
    RESOLVED = 2
    UPDATED = 3
    DEFERRED = 4
    CANCELED = 5
    COMMENTED = 6


class TicketEvent(db.model):
    """
    The event happened on ticket.\n
    Fields:\n
    id --> The id of the ticket, unique primary key.\n
    event_type --> The type of this event.\n
    ticket_id --> The ticket associated with this event, forien key.\n
    message --> The message associated with this event, nullable.\n
    is_anonymous --> Whether this update is anonymous.\n
    user_id --> The user that created this event.\n
    timestamp --> The timestamp of this event.\n
    """
    id = db.Column(db.Integer(20), primary_key=True, nullable=False)
    # need to change a name in db, since type is a presereved word in python
    event_type = db.Column(db.Integer(11), nullable=False)
    ticket_id = db.Column(db.Integer(20), db.ForeignKey('ticket.id'),
                          nullable=False)
    message = db.Column(db.String(255), nullable=True)
    is_anonymous = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer(20), db.ForeignKey('user.id'),
                        nullable=False)
    timestamp = db.Column(db.Datetime, nullable=False, default=datetime.now())

    # Getter Methods
    # Checking event types
    def is_create(self) -> bool:
        """
        Check if the event type is create.\n
        Return:\n
        Bool indicating if it its create type.\n
        """
        return self.event_type == EventType.CREATED

    def is_accepted(self) -> bool:
        """
        Check if the event type is accepted.\n
        Return:\n
        Bool indicating if it its accepted type.\n
        """
        return self.event_type == EventType.ACCEPTED

    def is_resolved(self) -> bool:
        """
        Check if the event type is resolved.\n
        Return:\n
        Bool indicating if it its resolved type.\n
        """
        return self.event_type == EventType.RESOLVED

    def is_update(self) -> bool:
        """
        Check if the event type is update.\n
        Return:\n
        Bool indicating if it its update type.\n
        """
        return self.event_type == EventType.UPDATED

    def is_deffered(self) -> bool:
        """
        Check if the event type is deffered.\n
        Return:\n
        Bool indicating if it its deffered type.\n
        """
        return self.event_type == EventType.DEFERRED

    def is_canceled(self) -> bool:
        """
        Check if the event type is canceled.\n
        Return:\n
        Bool indicating if it its canceled type.\n
        """
        return self.event_type == EventType.CANCELED

    def is_commented(self) -> bool:
        """
        Check if the event type is commented.\n
        Return:\n
        Bool indicating if it its commeneted type.\n
        """
        return self.event_type == EventType.COMMENTED

    def reveal_user(self, user: User, course: Course) -> bool:
        """
        Determine whether this event can be revealed to a user.\n
        Inputs:\n
        user --> The user object to be determined.\n
        course --> The course of this user & of this ticket is in.\b
        Return:\n
        bool value of whether this can be viewed by this user.\n
        """
        # Need methods from enrolledcourse and user.
    
    # Not implemnting (since not used):
    # findAllForTutor


# static query methods
def find_all_events_for_ticket(ticket: Ticket) -> List[TicketEvent]:
    """
    Find all the ticket events associated to a ticket.\n
    Inputs:\n
    ticket --> The ticket object to be look for.\n
    Return:\n
    A list of event related to this ticket.\n
    """
    return TicketEvent.query().filter_by(ticket_id=ticket.id)\
        sort_by(TicketEvent.timestamp).desc.all()


def find_all_events_for_tickets(tickets: List[Ticket]) -> List[TicketEvent]:
    """
    Find all the ticket events of multiple tickets.\n
    Inputs:\n
    tickets --> A list of ticktes.\n
    Return:\n
    A list of event related to the tickets passed in.\n
    """
    result_list = []
    for ticket in tickets:
        result_list += find_all_events_for_ticket(ticket)
    return result_list
