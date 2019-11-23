from app import db
from enum import Enum
from typing import List
from datetime import datetime
from operator import attrgetter
from user import User
from enrolled_course import EnrolledCourse, fake_getrole, Role  # Pretending
from course import Course # Pretending
from ticket_feedback import TicketFeedback # Pretending
from ticket_event import TicketEvent # Pretending


"""
Note for implementation:
For all the queries methods in Ticket.java when it related to queue\
I will implement it in the queue.py instead of here.\n

"""

# Only 3 tags allowed per ticket
MAX_TAG_NUM = 3
# IF the room is not in cse building, the front end should pass in NON_CSE
NON_CSE = 'NON_CSE'
# IF the room is not in cse building, the front end should pass in HALLWAY
HALLWAY = 'HALLWAY'


class Status(Enum):
    """
    The status of the ticket with the following options --> database value:\n
    PENDING --> 0\n
    ACCEPTED --> 1\n
    RESOLVED --> 2\n
    CANCELED --> 3\n
    """
    PENDING = 0
    ACCEPTED = 1
    RESOLVED = 2
    CANCELED = 3


class HelpType (Enum):
    """
    The type of the help the student need for this ticket\
        with the following options --> database value:\n
    Question --> 0\n
    Checkoff --> 1\n
    """
    QUESTION = 0
    CHECKOFF = 1


class TicketTag (Enum):
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


class Ticket(db.Model):
    """
    The ticket model of the database.
    Fields:
    id --> The id of the ticket, unique primary key.\n
    created_at --> The time that this ticket is created.\n
    closed_at --> The time that this ticket is closed. Nullable\n
    room --> The room that this student is in.\n
    workstaton --> The workstation of the student.\n
    status --> The status of this ticket.\n
    title --> The title of this ticket.\n
    description --> The discription of the ticket created by student.\n
    grader_id --> The grader_id who accepted this ticket, Nullable.\n
    student_id --> The student_id who created this ticket.\n
    is_private --> Whether this ticket is private.\n
    accepted_at --> The time that this ticket was accepted.\n
    help_type --> The type of help student need.\n
    tag_one --> The ticket tag for this ticket. Not nullable since at least\
                a tag.\n
    tag_two --> The ticket tag for this ticket. Nullable.\n
    tag_three --> The ticket tag for this ticket. Nullable.\n
    """
    __tablename__ = 'Ticket'
    id = db.Column(db.Integer(20), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, nullabble=True)
    closed_at = db.Column(db.DateTime, nullabble=True)
    room = db.Column(db.String(255), nullable=False)
    workstaton = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer(11), nullable=False,
                       default=Status.PENDING)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    grader_id = db.Column(db.Integer(20), db.ForeignKey('user.id'),
                          nullable=True)
    queue_id = db.Column(db.Integer(20, db.ForeignKey('queue.id'),
                         nullable=False))
    student_id = db.Column(db.Integer(20), db.ForeignKey('user.id'),
                           nullable=False)
    is_private = db.Column(db.Boolean, nullable=False)
    accepted_at = db.Column(db.DateTime, nullabble=True)
    help_type = db.Column(db.Integer(11), nullable=False)
    tag_one = db.Column(db.Integer(20), db.ForeignKey('ticket_tag.id'),
                        nullable=False)
    tag_two = db.Column(db.Integer(20), db.ForeignKey('ticket_tag.id'),
                        nullable=True)
    tag_three = db.Column(db.Integer(20), db.ForeignKey('ticket_tag.id'),
                          nullable=True)

    # All the getter methods / status checking methods:
    def is_question(self) -> bool:
        """
        Return if the ticket is a question or not.\n
        Return:\n
        A bool value determing if it is a question.\n
        """
        return self.help_type == HelpType.QUESTION

    def is_checkoff(self) -> bool:
        """
        Return if the ticket is a checkoff or not.\n
        Return:\n
        A bool value determing if it is a checkoff.\n
        """
        return self.help_type == HelpType.CHECKOFF

    def is_pending(self) -> bool:
        """
        Return if the ticket is pending or not.\n
        Return:\n
        A bool value determing if it is pending.\n
        """
        return self.status == Status.PENDING

    def is_accepted(self) -> bool:
        """
        Return if the ticket is accepted or not.\n
        Return:\n
        A bool value determing if it is accepted.\n
        """
        return self.status == Status.ACCEPTED

    def is_resolved(self) -> bool:
        """
        Return if the ticket is resolved or not.\n
        Return:\n
        A bool value determing if it is resolved.\n
        """
        return self.status == Status.RESOLVED

    def is_canceled(self) -> bool:
        """
        Return if the ticket is canceled or not.\n
        Return:\n
        A bool value determing if it is canceled.\n
        """
        return self.status == Status.CANCELED

    def is_non_cse(self) -> bool:
        """
        Return if the ticket is not in CSE building or not.\n
        Return:\n
        A bool value determing if it is in CSE.\n
        """
        return self.room == NON_CSE

    def is_hallway(self) -> bool:
        """
        Return if the ticket is located at hallway.\n
        Return:\n
        A bool value determing if it is in the hallway.\n
        """
        return self.room == HALLWAY

    def get_tags_list(self) -> List[TicketTag]:
        """
        Return if the list of the tags that is on this ticket.\n
        Return:\n
        An array of size 1 to 3 with ticket tags in it.\n
        """
        return self.room == HALLWAY

    def get_help_time_in_second(self) -> float:
        """
        Get the time in second of the time that this ticket spent\
        to be resolved.\n
        Return:\n
        The difference in time.\n
        """
        return (self.closed_at - self.created_at).total_second()

    def get_title(self) -> str:
        """
        Return the title of the ticket.\n
        Return:\n
        The title in string.\n
        """
        return self.title

    def get_position(self) -> int:
        """
        Return the position of the ticket in the current queue.\n
        Return:\n
        The position of the ticket (start from 1).\n
        """
        all_pending_tickets = Ticket.query.filter_by(
                                queue_id=self.queue_id,
                                status=Status.PENDING
                                ).all()
        all_pending_tickets.sort(key=attrgetter('created_at'))
        return all_pending_tickets.index(self) + 1

    # Get addition info outside the class
    def has_feedback(self) -> bool:
        """
        Check if this ticket has feedback.\n
        Return:\n
        Bool of saying if the ticket has a feedback or not.\n
        """
        if (self.get_latest_feedback() is None):
            return False

    def get_latest_feedback(self) -> TicketFeedback:
        """
        Get the latest feedback of this ticket.\n
        Return:\n
        The latest TicketFeedback Object.\n
        """
        return TicketFeedback.query.filter_by(
                ticket_id=self.ticket_id).order_by(
                TicketFeedback.submitted_date).first()

    def get_ticket_events(self) -> List[TicketEvent]:
        """
        Get the events that are happened on this ticket.
        Return:\n
        A list of the events happend on this ticket.
        """
        return TicketEvent.query.filter_by(
                ticket_id=self.id).order_by(id).all()

    # Permission of the ticket that a user has
    def can_view_by(self, user: User) -> bool:
        """
        Determine if the ticket can be viewed by a given user.\n
        Inputs:\n
        The User object of the user who is trying to view the ticket.\n
        Return:\n
        The bool for whether a user can view.\n
        """
        if (user is None):
            return False
        elif (not self.is_private):
            return True
        else:
            course = Course.query.filter_by(queue_id=self.queue_id).first()
            if (fake_getrole(user.id, course.id) == Role.STAFF):
                return True
            else:
                if (self.student_id == user.id):
                    return True
                else:
                    return False

    def can_edit_by(self, user: User) -> bool:
        """
        Determine if the ticket can be edited by a given user.\n
        Inputs:\n
        The User object of the user who is trying to edit the ticket.\n
        Return:\n
        The bool for whether a user can edit.\n
        """
        if (self.is_resolved()):
            return False
        else:
            course = Course.query.filter_by(queue_id=self.queue_id).first()
            if (fake_getrole(user.id, course.id) == Role.STAFF):
                return True
            else:
                if (self.student_id == user.id):
                    return True
                else:
                    return False

    def update_ticket_tags(self, tag_list: List[TicketTag]) -> None:
        """
        Update the tags on the ticket.\n
        Input:\n
        tag_list --> The list of tags in which everything is of the type\
                     TicketTag.\n
        """
        # Update the tags
        self_tag_list = []
        for i in range(0, MAX_TAG_NUM):
            if (i < len(tag_list)):
                self_tag_list.append(tag_list[i])
            else:
                self_tag_list.append(None)

        # Assign the instance tags from the list
        self.tag_one = self_tag_list[0]
        self.tag_two = self_tag_list[1]
        self.tag_three = self_tag_list[2]

        # Update the database
        db.session.commit()

    # Setter functions
    def mark_pending(self) -> None:
        """
        Mark the ticket as pending status.\n
        """
        self.status = Status.PENDING
        db.session.commit()

    def mark_accepted_by(self, grader_id: int) -> None:
        """
        Mark the ticket as accepted by a tutor.\n
        """
        self.status = Status.ACCEPTED
        self.accepted_at = datetime.now()
        self.grader_id = grader_id
        db.session.commit()

    def mark_resolved(self) -> None:
        """
        Mark the ticket as resolved.\n
        """
        self.status = Status.RESOLVED
        self.closed_at = datetime.now()
        db.session.commit()

    def mark_canceled(self) -> None:
        """
        Mark the ticket as canceled.\n
        """
        self.status = Status.CANCELED
        self.closed_at = datetime.now()
        db.session.commit()

    def student_update(self, title: str, description: str, room: str,
                       workstation: str, isPrivate: bool, help_type: HelpType,
                       tag_list: List[TicketTag]) -> None:
        """
        This method updates the current ticket. By taking in the updates from
        front end, this will update the corresponding tickit in the database.
        Inputs:
        title --> The title of the ticket.\n
        description --> The description of the ticket.\n
        room --> The room that the student is in.\n
        workstation --> The workstation of the student.\n
        ipPrivate --> Whether the student want this ticket to be private.\n
        help_type --> The type of help the student demends.\n
        """
        # Perform update for all the basic info
        self.title = title
        self.description = description
        self.room = room
        self.workstation = workstation
        self.isPrivate = isPrivate
        self.help_type = help_type

        # Commit the updates for basica info
        db.session.commit()

        # Update ticket tags
        self.update_ticket_tags(tag_list)
