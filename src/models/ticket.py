from app import db
from enum import Enum
from typing import List, Optional
from datetime import datetime, timedelta
from operator import attrgetter
from user import User
from enrolled_course import EnrolledCourse, fake_getrole, Role  # Pretending
from course import Course # Pretending
from ticket_feedback import TicketFeedback # Pretending
from ticket_event import TicketEvent # Pretending
from queue import Queue


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
    @author YixuanZhou
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
    @author YixuanZhou
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
    @author YixuanZhou
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
    created_at --> The time that this ticket is created,
                   default is the current time.\n
    closed_at --> The time that this ticket is closed. Nullable\n
    room --> The room that this student is in.\n
    workstaton --> The workstation of the student.\n
    status --> The status of this ticket.\n
    title --> The title of this ticket.\n
    description --> The discription of the ticket created by student.\n
    grader_id --> The grader_id who accepted this ticket, Nullable.\n
    queue_id --> The queue_id of which this ticket belongs to.\n
    student_id --> The student_id who created this ticket.\n
    is_private --> Whether this ticket is private.\n
    accepted_at --> The time that this ticket was accepted.\n
    help_type --> The type of help student need.\n
    tag_one --> The ticket tag for this ticket. Not nullable since at least\
                a tag.\n
    tag_two --> The ticket tag for this ticket. Nullable.\n
    tag_three --> The ticket tag for this ticket. Nullable.\n
    @author YixuanZhou
    """
    __tablename__ = 'Ticket'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)
    closed_at = db.Column(db.DateTime, nullable=True, deafult=None)
    room = db.Column(db.String(255), nullable=False)
    workstaton = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False,
                       default=Status.PENDING)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    grader_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=True, default=None)
    queue_id = db.Column(db.Integer, db.ForeignKey('queue.id'),
                         nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                           nullable=False)
    is_private = db.Column(db.Boolean, nullable=False)
    accepted_at = db.Column(db.DateTime, nullable=True, default=None)
    help_type = db.Column(db.Integer, nullable=False)
    tag_one = db.Column(db.Integer, nullable=False)
    tag_two = db.Column(db.Integer, nullable=True, default=None)
    tag_three = db.Column(db.Integer, nullable=True, default=None)

    def __init__(self, **kwargs):
        """
        The constructor of the ticket object.\n
        Inputs:\n
        created_at --> The time that ticket is created, default is None.\n
        room --> The room that this ticket is in.\n
        workstation --> the workstation that the ticket at.\n
        title --> The title of this ticket.\n
        description --> The description of this ticket.\n
        queue_id --> The queue it for that queue.\n
        student_id --> The student_id of the student who created the ticket.\n
        is_private --> Wheather this ticket is private.\n
        helpy_type --> The type of help student demands.\n
        tag_one --> The first tag to the ticket.\n
        tag_two --> The second tag (default is none) to the ticket.\n
        tag_three --> The third tag (dfault is none) to the ticket.\n
        """
        super(Ticket, self).__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Save the changes made to the object into the database.\n
        """
        db.seesion.commit()

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
        ticket_tag = []
        ticket_tag.append(self.tag_one)
        if (self.tag_two is not None):
            ticket_tag.append(self.tag_two)
        if (self.tag_three is not None):
            ticket_tag.append(self.tag_three)
        return ticket_tag

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

    def get_latest_feedback(self) -> Optional[TicketFeedback]:
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
        user --> The User object of the user who is trying to view the 
        ticket.\n
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
        user --> The User object of the user who is trying to edit the
        ticket.\n
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
        self.save()

    # Setter functions
    def mark_pending(self) -> None:
        """
        Mark the ticket as pending status.\n
        """
        self.status = Status.PENDING
        self.save()

    def mark_accepted_by(self, grader_id: int) -> None:
        """
        Mark the ticket as accepted by a tutor.\n
        """
        self.status = Status.ACCEPTED
        self.accepted_at = datetime.now()
        self.grader_id = grader_id
        self.save()

    def mark_resolved(self) -> None:
        """
        Mark the ticket as resolved.\n
        """
        self.status = Status.RESOLVED
        self.closed_at = datetime.now()
        self.save()

    def mark_canceled(self) -> None:
        """
        Mark the ticket as canceled.\n
        """
        self.status = Status.CANCELED
        self.closed_at = datetime.now()
        self.save()

    def student_update(self, title: str, description: str, room: str,
                       workstation: str, is_private: bool, help_type: HelpType,
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
        self.is_private = is_private
        self.help_type = help_type

        # Commit the updates for basica info
        self.save()

        # Update ticket tags
        self.update_ticket_tags(tag_list)


# Note:
# So far not implementing the methods used by controllers, including
# findOldestForQueue
# findNewestForQueue
# findOldestForQueueForGrader
# findNewestForQueueForGrader
# findNewestForStudent
# For NewsFeedPost including:
# findResolvedTicketsForQueueForGraderAfter
# findLastResolvedTicketForQueueForGrader
# For TicketFeedback:
# findNewestFeedback should be in TicketFeedback

def find_all_tickets(queue: Queue,
                     status: List[Status] = None) -> List[Ticket]:
    """
    Get a list of all the tickets for a queue with decending order
    by the time it was created.\n
    Input:\n 
    queue --> The queue to search for.\n
    status --> Optional params for finding tickets with specific list status.\n
    Return:\n
    The list of the ticket of this queue ordered by create time.\n
    """
    if status:
        return Ticket.query.\
            filter_by(queue_id=queue.id).\
            order_by(Ticket.created_at).desc.all()
    else:
        return Ticket.query.\
            filter_by(queue_id=queue.id).filter_by(status.in_(status)).\
            order_by(Ticket.created_at).desc.all()


def find_all_tickets_by_student(queue: Queue,
                                student: User,
                                status: List[Status]) -> List[Ticket]:
    """
    Get a list of all the tickets for a queue created by a student
    with decending order by the time it was created.\n
    Input:\n
    queue --> The queue to search for.\n
    student --> The student to be looked for.\n
    status --> The list of status to filter.\n
    Return:\n
    The list of the ticket of this queue ordered by create time.\n
    """
    return Ticket.query.\
        filter_by(queue_id=queue.id, student_id=student.id).\
        filter_by(status.in_(status)).\
        order_by(Ticket.created_at).desc.all()


def find_all_tickets_for_grader(queue: Queue, grader: User) -> List[Ticket]:
    """
    Get a list of all the tickets for a queue handled by a grader
    with decending order by the time it was created.\n
    Input:\n 
    queue --> The queue to search for.\n
    grader --> The grader to be looked for.\n
    Return:\n
    The list of the ticket of this queue ordered by create time.\n
    """
    return Ticket.query.\
        filter_by(queue_id=queue.id, grader_id=grader.id).\
        order_by(Ticket.created_at).desc.all()


def find_tickets_in_range(queue: Queue, start: datetime,
                          end: datetime, grader: User = None) -> List[Ticket]:
    """
    Find all the ticktes of the queue in range of two datetimes.\n
    Input:\n
    queue_id --> The id of the queue to look at.\n
    grader --> An optional User object, use it if want to find for a grader.\n
    start --> The begining of the range,
              it would be 1 hour before by default.\n
    end --> The end of the range, it would be now by default.\n
    Return:\n
    A list of tickets in this range.\n
    """
    if (grader is None):
        ticket_list = Ticket.query.filter_by(queue=queue.id,
                                             status=Status.RESOLVED).all()
    else:
        ticket_list = Ticket.query.filter_by(queue_id=queue.id,
                                             grader_id=grader.id,
                                             status=Status.RESOLVED).all()
    if (start is None):
        start = datetime.now() - timedelta(hours=1)
    if (end is None):
        end = datetime.now()
    return list(filter(lambda x: start <= x.closed_at <= end, ticket_list))


def find_ticket_accpeted_by_grader(grader: User) -> Optional[Ticket]:
    """
    Find the last ticket accepted by the grader.\n 
    There should only be one ticket that is accpeted by the grader.\n
    Inputs:\n
    grader --> The User object of the grader to look up.\n
    Return:\n
    The ticket that was accepted by the grader.\n
    """
    return Ticket.query.filter_by(status=Status.ACCEPTED,
                                  grader_id=grader.id).first()


def find_resolved_tickets_in(queue: Queue, recent_hour: bool = False,
                             day: bool = False,
                             start: datetime = None,
                             end: datetime = None) -> List[Ticket]:
    """
    Get the tickets for the queue that were reolsved.\n
    Inputs:\n
    queue --> the id of the queue to look at.\n
    recent --> If you want for the recent hour (1st priority).\n
    day --> If you want for only today (2nd priority).\n
    start --> If you want a specific start time, default is None.\n
    end --> For a specifice end time, default is None.\n
    Return:\n
    A list of tickets resolved for this queue given a certain range (or not).\n
    """
    ticket_list = Ticket.query.filter_by(queue_id=queue.id,
                                         status=Status.RESOLVED).all()
    if (recent_hour):
        now = datetime.now()
        lasthour = datetime.now() - timedelta(hours=1)
        return find_tickets_in_range(queue=queue, start=lasthour, end=now)
    elif (day):
        return list(filter(lambda x: x.closed_at == datetime.today(),
                           ticket_list))
    else:
        return find_tickets_in_range(queue=queue, start=start, end=end)
        return ticket_list


def find_ticket_history_with_offset(queue: Queue, offset: int = 0,
                                    limit: int = 10,
                                    student: User = None,
                                    grader: User = None) -> List[Ticket]:
    """
    Find a list of tickets with certain offsets and limits with the order of
    ticket_id.\n
    Inputs:\n
    queue --> The queue to look up.\n
    offset --> The offset to start looking up.\n
    limit --> The limit of to display.\n
    Return:\n
    A list of tickets.
    """
    if (student is not None):
        return Ticket.query().filter_by(queue_id=queue.id).\
            filter_by(Ticket.status.in_(Status.RESOLVED,
                                        Status.CANCELED)).\
            filter_by(student_id=student.id).\
            sort_by(id).offset(offset).limit(limit).all()
    elif (grader is not None):
        return Ticket.query().filter_by(queue_id=queue.id).\
            filter_by(Ticket.status.in_(Status.RESOLVED,
                                        Status.CANCELED)).\
            filter_by(grader_id=grader.id).\
            sort_by(id).offset(offset).limit(limit).all()
    else:
        Ticket.query().filter_by(queue_id=queue.id).\
            filter_by(Ticket.status.in_(Status.RESOLVED,
                                        Status.CANCELED)).\
            sort_by(id).offset(offset).limit(limit).all()


# Ticket stats calultaions
def average_resolved_time(resolved_tickets: List[Ticket]) -> int:
    """
    Given a list of tickest, get the average time in second for resolve time.\n
    Inputs:\n
    resolved_tickets --> a list of tickests that has been resolved.\n
    Return:\n
    The number of the average time in seconds.\n
    """
    sum_time = 0
    for ticket in resolved_tickets:
        sum_time += ticket.get_help_time_in_second()
    return (int)(sum_time / len(resolved_tickets))


# Do we need it?
def defer_accpeted_ticket_for_grader(grader: User) -> None:
    """
    Set all the accepted ticket for a grader to pending incase multiple
    tickets is accepted by one grader.\n
    Inputs:\n
    grader --> The grader to be multified.\n
    """
    ticket_list = Ticket.query.filter_by(grader_id=grader.id).all()
    for ticket in ticket_list:
        ticket.mark_pending()
