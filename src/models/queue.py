from app import db
from enum import Enum
from user import User
import ticket as t
from models.events.ticket_event import TicketEvent, EventType
from typing import List, Optional
from datetime import datetime, timedelta
from course import Course # pretending
import news_feed_post as nfp # pretending


"""
Define Constant
"""
DEFAULT_WAIT_TIME = timedelta(minutes=12)  # 12min
MIN_WAIT_TIME = timedelta(minutes=5)  # 5min


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
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    high_capacity_enabled = db.Column(db.Boolean, nullable=False, default=True)
    high_capacity_threshold = db.Column(db.Integer, nullable=False,
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
    ticket_cooldown = db.Column(db.Integer, nullable=False, default=10)

    def add_ticket(self, student: User, title: str,
                   description: str, room: str,
                   workstation: str, is_private: bool,
                   help_type: t.HelpType,
                   tag_list: List[t.TicketTag]) -> t.Ticket:
        """
        Add a ticket.\n
        Inputs:\n
        student --> The student who submit the ticket.\n
        title --> The title of the ticket.\n
        description --> The description to the ticket.\n
        room --> The room of this ticket is in.\n
        workstation --> The workstaton ticket is at.\n
        help_type --> The type of help needed.\n
        tag_list --> The list of tags of the tickte.\n
        Return:\n
        The created ticket.\n
        """
        tag_one = tag_list[0]
        tag_two = tag_list[1] if len(tag_list) > 1 else None
        tag_three = tag_list[2] if len(tag_list) > 2 else None
        new_ticket = t.Ticket(created_at=datetime.now(), closed_at=None,
                              room=room, workstation=workstation,
                              title=title, description=description,
                              grader_id=None, queue_id=self.id,
                              student_id=student.id, is_private=is_private,
                              accepted_at=None, help_type=help_type,
                              tag_one=tag_one, tag_two=tag_two,
                              tag_three=tag_three)
        return new_ticket

    def update_ticket(self, student: User, title: str,
                      description: str, room: str,
                      workstation: str, is_private: bool,
                      help_type: t.HelpType,
                      tag_list: List[t.TicketTag]) -> t.Ticket:
        """
        Update a ticket if exist or add.\n
        Inputs:\n
        student --> The student who submit the ticket.\n
        title --> The title of the ticket.\n
        description --> The description to the ticket.\n
        room --> The room of this ticket is in.\n
        workstation --> The workstaton ticket is at.\n
        help_type --> The type of help needed.\n
        tag_list --> The list of tags of the tickte.\n
        Return:\n
        The updated ticket.\n
        """
        old_ticket = t.find_pending_ticket_by_student(queue=self,
                                                      student=student)
        if (old_ticket is not None):
            old_ticket.student_update(title=title, description=description,
                                      room=room, workstation=workstation,
                                      is_private=is_private,
                                      help_type=help_type,
                                      tag_list=tag_list)
            # Create a new Ticket Event
            TicketEvent(event_type=EventType.UPDATED,
                        ticket_id=old_ticket.id, user_id=student.id)
            return old_ticket
        else:
            return self.add_ticket(student=student, title=title,
                                   description=description, room=room,
                                   workstation=workstation,
                                   is_private=is_private,
                                   help_type=help_type, tag_list=tag_list)

    # Getter Methods for Queue Status
    def is_open(self) -> bool:
        """
        Check if the queue is open.\n
        Return:\n
        bool value indicates queue is open or not.\n
        """
        return self.status == Status.OPEN

    def is_locked(self) -> bool:
        """
        Check if the queue is locked.\n
        Return:\n
        bool value indicates queue is locked or not.\n
        """
        return self.status == Status.LOCKED

    def is_closed(self) -> bool:
        """
        Check if the queue is closed.\n
        Return:\n
        bool value indicates queue is closed or not.\n
        """
        return self.status == Status.CLOSED

    # Status setter methods
    def open(self) -> None:
        """
        Open the queue.
        """
        self.status = Status.OPEN
        db.session.commit()

    def lock(self) -> None:
        """
        Lock the queue.
        """
        self.status = Status.LOCKED

    def close(self) -> None:
        """
        Close the queue.
        """
        self.status = Status.CLOSED

    def clear_ticket(self) -> None:
        """
        Clear all the tickets in the queue.
        """
        unresolved_tickets = t.find_all_tickets(self, [t.Status.PENDING])

        for ticket in unresolved_tickets:
            ticket.mark_canceled()

    def __repr__(self) -> str:
        """
        The to string method to return which course this queue belongs to.\n
        Returns:\n
        The string representation of the course it belongs to.\n
        """
        course = Course.query().filter_by(course_id=self.course_id)
        if (course is not None):
            return repr(course)
        else:
            return None

    # Get tickets / tickets related sttaus
    def get_pending_tickets(self) -> List[t.Ticket]:
        """
        Get all the penidng tickets of the queue.\n
        Results:\n
        A list of tickets that is pending in this queue.\n
        """
        return t.find_all_tickets(self, status=[t.Status.PENDING])

    def get_accepted_tickets(self) -> List[t.Ticket]:
        """
        Get all the accepted tickets of the queue.\n
        Results:\n
        A list of tickets that is accepted in this queue.\n
        """
        return t.find_all_tickets(self, status=[t.Status.ACCEPTED])

    def get_unresolved_tickets(self) -> List[t.Ticket]:
        """
        Get all the unresolved tickets of the queue.\n
        Results:\n
        A list of tickets that is either pending or accepeted.\n
        """
        return t.find_all_tickets(self, status=[t.Status.PENDING,
                                                t.Status.ACCEPTED])

    def get_resolved_tickets(self) -> List[t.Ticket]:
        """
        Get all the resolved tickets of the queue.\n
        Results:\n
        A list of tickets that is resolved.\n
        """
        return t.find_all_tickets(self, status=[t.Status.RESOLVED])

    def get_canceled_tickets(self) -> List[t.Ticket]:
        """
        Get all the canceled tickets of the queue.\n
        Results:\n
        A list of tickets that is canceled.\n
        """
        return t.find_all_tickets(self, status=[t.Status.CANCELED])

    def is_at_high_capacity(self) -> bool:
        """
        Check if the queue is at high capacity.\n
        Return:\n
        bool value indicates queue is at high capacity or not.\n
        """
        threshold = self.high_capacity_threshold
        return self.high_capacity_enabled and\
            len(self.get_unresolved_tickets(self)) > threshold

    def get_closed_ticktes_history(self, page_num: int = 0,
                                   num_per_page: int = 10) -> List[t.Ticket]:
        """
        Get the closed tickte history of page.\n
        Inputs:\n
        page_num --> The page to start looking at, default 0.\n
        num_per_page --> The number of entries to list per page, default 10.\n
        Returns:\n
        List of closed tickets history.\n
        """
        offset = page_num * num_per_page
        return t.find_ticket_history_with_offset(queue=self,
                                                 offset=offset,
                                                 limit=num_per_page)

    def get_closed_ticket_history_for(self, student: User, page_num: int = 0,
                                      num_per_page: int = 10) \
            -> List[t.Ticket]:
        """
        Get the closed tickte history of page for a student.\n
        Inputs:\n
        student --> The User object for the student.\n
        page_num --> The page to start looking at, default 0.\n
        num_per_page --> The number of entries to list per page, default 10.\n
        Returns:\n
        List of closed tickets history for a student.\n
        """
        offset = page_num * num_per_page
        return t.find_ticket_history_with_offset(queue=self,
                                                 offset=offset,
                                                 limit=num_per_page,
                                                 student=student)

    def get_pending_ticket_for(self, student: User) -> Optional[t.Ticket]:
        """
        Get a pending ticket for a certain student on this queue.
        (There should only be one pending ticket).
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        The pending ticket of the student on this queue.\n
        """
        return t.find_all_tickets_by_student(queue=self, student=student,
                                             status=[t.Status.PENDING])[0]

    def get_accepted_ticket_for(self, student: User) -> Optional[t.Ticket]:
        """
        Get an accepted ticket for a certain student on this queue.
        (There should only be one pending ticket).
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        The pending ticket of the student on this queue.\n
        """
        return t.find_all_tickets_by_student(queue=self, student=student,
                                             status=[t.Status.ACCEPTED])[0]

    def get_unresolved_ticket_for(self, student: User) -> Optional[t.Ticket]:
        """
        Get an unresolved ticket for a certain student on this queue.
        (There should only be one pending ticket).
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        The pending ticket of the student on this queue.\n
        """
        return t.find_all_tickets_by_student(queue=self, student=student,
                                             status=[t.Status.ACCEPTED,
                                                     t.Status.PENDING])[0]

    def get_resolved_ticket_for(self, student: User) -> List[t.Ticket]:
        """
        Get an resolved ticket for a certain student on this queue.
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        A list of tickets of the student on this queue that are resolved.\n
        """
        return t.find_all_tickets_by_student(queue=self, student=student,
                                             status=[t.Status.RESOLVED])

    def get_canceled_ticket_for(self, student: User) -> List[t.Ticket]:
        """
        Get an canceled ticket for a certain student on this queue.
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        A list of tickets of the student on this queue that are resolved.\n
        """
        return t.find_all_tickets_by_student(queue=self, student=student,
                                             status=[t.Status.CANCELED])

    # Not implementing getLastResolvedTicketFor since it was only used
    # In tickets stats which is already handled.

    # Student bool query methods
    def has_pending_tickect_for(self, student: User) -> bool:
        """
        Check whether this student has a pending ticket in this queue.\n
        Inputs:\n
        student --> The student object to look for.\n
        Returns:\n
        A bool value indicate whether there is or there is not a pending
        ticekct.\n
        """
        return self.get_pending_ticket_for(student) is not None
    
    def has_accepted_tickect_for(self, student: User) -> bool:
        """
        Check whether this student has an accepted ticket in this queue.\n
        Inputs:\n
        student --> The student object to look for.\n
        Returns:\n
        A bool value indicate whether there is or there is not a pending
        ticekct.\n
        """
        return self.get_accepted_ticket_for(student) is not None

    def has_unresolved_tickect_for(self, student: User) -> bool:
        """
        Check whether this student has an accepted ticket in this queue.\n
        Inputs:\n
        student --> The student object to look for.\n
        Returns:\n
        A bool value indicate whether there is or there is not a pending
        ticekct.\n
        """
        return self.get_unresolved_ticket_for(student) is not None

    # Grader Ticket Queuery Methods
    def get_ticket_accepted_by(self, grader: User, all: bool = False) \
            -> List[t.Ticket]:
        """
        Get tickes accepted by a grader with a choice of how many tickest to
        look for.\n
        Inputs:\n
        grader --> The grader to search for.\n
        all --> Indicate you whether all tickets are returned.\n
        Returns:\n
        A list of tickects that is accepted by the grader
        (If only one is needed, the ticket will be the first one and
        the only one in the list).\n
        """
        if (all):
            return t.find_all_ticket_accpeted_by_grader(self, grader=grader)
        else:
            return [t.find_ticket_accpeted_by_grader(self, grader=grader)]

    def get_ticket_resolved_by(self, grader: User) -> List[t.Ticket]:
        """
        Get all the tickes resolved by a grader.
        Inputs:\n
        grader --> The grader to search for.\n
        Returns:\n
        A list of tickest that is resolved by the grader.\n
        """
        tickets = t.find_all_tickets_for_grader(self, grader)
        return list(filter(lambda x: x.status == t.Status.RESOLVED), tickets)

    # Grader tickets bool query methods
    def has_ticket_accepted_by(self, grader: User) -> bool:
        return len(self.get_ticket_accepted_by(grader)) != 0

    # News feed post functionalities
    def get_news_feed_post(self, num: int = 20) -> List[nfp.NewsFeedPost]:
        """
        Get the news feed post on the queue.
        Inputs:\n
        num --> The number of news feed posts to look up for.
        Returns:\n
        A list of news feed post.
        """
        # nfp.find...
        pass

    def get_archived_news_feed_post(self, num: int = 20)\
            -> List[nfp.NewsFeedPost]:
        """
        Get the archeived news feed posts for the queue.
        Inputs:\n
        Inputs:\n
        num --> The number of news feed posts to look up for.
        Returns:\n
        A list of archived news feed post.
        """
        # nfp.find...
        pass

    # Impelementing Queue Stats
    def average_help_time(self, day: bool = True, hour: bool = False,
                          start: datetime = None) -> timedelta:
        """
        Get the average help time within a time period for tickes in
        the queue.\n
        Inputs:\n
        day --> To look for a day, default would be true.\n
        hour --> To look for the recent hour, default would be false.\n
        start --> The start time to look for. The default would be None.
                  If start is provided, it has priority among hour and day.\n
        Returns:\n
        A timedelta object representing the averge help time for the tickes
        given that period.\n
        """
        if (start is not None):
            day = False
            hour = False
        tickets = t.find_resolved_tickets_in(self, day=day,
                                             hour=hour, start=start)
        if (len(tickets) < 5):
            return MIN_WAIT_TIME
        average_resolved_time = t.average_resolved_time(tickets)
        return timedelta(seconds=average_resolved_time)

    # getExpectedTimeUntilAvailableTutor need a query method probably in
    # enrolled classs...

    # TODO
    # Finish up queue stats
    # Login and Logout for the user (Grader)


# None Memeber Queue Methods
def find_current_queue_for_user(user: User) -> List[Queue]:
    """
    Find all the queues that this user is in currently.
    Inputs:\n
    user --> The User object to look for.
    Returns:\n
    A list of Queue that the user is in this quarter.
    """
    # TODO
    # Use the methods from enrolled class by using User methods to find
    # the enrolled classes of that user and fetch the queues of those classes.
    pass


def find_queue_for_course(course: Course) -> Optional[Queue]:
    """
    Find the queue corresponding for a course.
    Inputs:\n
    course --> the Course object to look for.
    Returns:\n
    The queue for that course, if a queue does not exist, None is return.\n
    """
    return Queue.query().filter(id=course.queue_id).first()
