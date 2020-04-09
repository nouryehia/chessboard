from __future__ import annotations
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime, timedelta

from ...setup import db

from .user import User
# from .user import Status as u_status
# from .course import Course
# from .course import Course
from .ticket import Ticket, TicketTag, HelpType
from .ticket import Status as t_status
from .events.ticket_event import TicketEvent, EventType
from .events.queue_login_event import QueueLoginEvent, ActionType

from .news_feed_post import NewsFeedPost
from .enrolled_course import EnrolledCourse


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
    @author YixuanZhou
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
    @author YixuanZhou
    """
    __tablename__ = 'Queue'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=Status.CLOSED)
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

    def __init__(self, **kwargs):
        """
        The constructor the queue object.\n
        Inputs:\n
        high_capacity_enabled --> Whether to enable high capacity or not.
                                  Default is true. \n
        high_capacity_enabled --> High capacity message. Default is provided.\n
        high_Capacity_waring --> The Warning to the student.
                                 Default is provided.\n
        ticket_cooldown --> The cooldown time for the ticket.\n
        """
        super(Queue, self).__init__(**kwargs)

    def save(self):
        """
        Save the object that is modified into the database.\n
        """
        db.session.commit()

    def add_ticket(self, student: User, title: str,
                   description: str, room: str,
                   workstation: str, is_private: bool,
                   help_type: HelpType,
                   tag_list: List[TicketTag]) -> Ticket:
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
        new_ticket = Ticket(created_at=datetime.now(), closed_at=None,
                            room=room, workstation=workstation,
                            title=title, description=description,
                            grader_id=None, queue_id=self.id,
                            student_id=student.id, is_private=is_private,
                            accepted_at=None, help_type=help_type,
                            tag_one=tag_one, tag_two=tag_two,
                            tag_three=tag_three)
        Ticket.add_to_db(new_ticket)
        return new_ticket

    def update_ticket(self, student: User, title: str,
                      description: str, room: str,
                      workstation: str, is_private: bool,
                      help_type: HelpType,
                      tag_list: List[TicketTag]) -> Ticket:
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
        old_ticket = Ticket.find_pending_ticket_by_student(queue=self,
                                                           student=student)
        if not old_ticket:
            old_ticket.student_update(title=title, description=description,
                                      room=room, workstation=workstation,
                                      is_private=is_private,
                                      help_type=help_type,
                                      tag_list=tag_list)
            # Create a new Ticket Event
            te = TicketEvent(event_type=EventType.UPDATED,
                             ticket_id=old_ticket.id,
                             user_id=student.id)
            TicketEvent.add_to_db(te)
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
        self.save()

    def lock(self) -> None:
        """
        Lock the queue.
        """
        self.status = Status.LOCKED
        self.save()

    def close(self) -> None:
        """
        Close the queue.
        """
        self.status = Status.CLOSED
        self.save()

    def clear_ticket(self) -> None:
        """
        Clear all the tickets in the queue.
        """
        unresolved_tickets = Ticket.find_all_tickets(self, [t_status.PENDING])

        for ticket in unresolved_tickets:
            ticket.mark_canceled()

    def __repr__(self) -> str:
        """
        The to_string method to return which course this queue belongs to.\n
        Returns:\n
        The string representation of the course it belongs to.\n
        """
        course = Course.query().filter_by(course_id=self.course_id)
        if not course:
            return repr(course)
        else:
            return None

    def to_json(self) -> Dict[str, str]:
        '''
        Function that takes a user object and returns it in dictionary.\n
        Params: none\n
        Returns: Dictionary of the user info
        '''
        ret = {}
        ret['queue_id'] = self.id
        ret['status'] = self.status
        ret['highCapacityEnabled'] = self.highCapacityEnabled
        ret['high_capacity_message'] = self.high_capacity_message
        ret['high_capacity_threshold'] = self.high_capacity_threshold
        ret['high_capacity_warning'] = self.high_capacity_warning
        ret['ticket_cooldown'] = self.ticket_cooldown
        return ret

    # Get tickets / tickets related sttaus
    def get_pending_tickets(self) -> List[Ticket]:
        """
        Get all the penidng tickets of the queue.\n
        Results:\n
        A list of tickets that is pending in this queue.\n
        """
        return Ticket.find_all_tickets(self, status=[t_status.PENDING])

    def get_accepted_tickets(self) -> List[Ticket]:
        """
        Get all the accepted tickets of the queue.\n
        Results:\n
        A list of tickets that is accepted in this queue.\n
        """
        return Ticket.find_all_tickets(self, status=[Status.ACCEPTED])

    def get_unresolved_tickets(self) -> List[Ticket]:
        """
        Get all the unresolved tickets of the queue.\n
        Results:\n
        A list of tickets that is either pending or accepeted.\n
        """
        return Ticket.find_all_tickets(self, status=[t_status.PENDING,
                                                     t_status.ACCEPTED])

    def get_resolved_tickets(self) -> List[Ticket]:
        """
        Get all the resolved tickets of the queue.\n
        Results:\n
        A list of tickets that is resolved.\n
        """
        return Ticket.find_all_tickets(self, status=[t_status.RESOLVED])

    def get_canceled_tickets(self) -> List[Ticket]:
        """
        Get all the canceled tickets of the queue.\n
        Results:\n
        A list of tickets that is canceled.\n
        """
        return Ticket.find_all_tickets(self, status=[t_status.CANCELED])

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
                                   num_per_page: int = 10) -> List[Ticket]:
        """
        Get the closed tickte history of page.\n
        Inputs:\n
        page_num --> The page to start looking at, default 0.\n
        num_per_page --> The number of entries to list per page, default 10.\n
        Returns:\n
        List of closed tickets history.\n
        """
        offset = page_num * num_per_page
        return Ticket.find_ticket_history_with_offset(queue=self,
                                                      offset=offset,
                                                      limit=num_per_page)

    def get_closed_ticket_history_for(self, student: User, page_num: int = 0,
                                      num_per_page: int = 10) \
            -> List[Ticket]:
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
        return Ticket.find_ticket_history_with_offset(queue=self,
                                                      offset=offset,
                                                      limit=num_per_page,
                                                      student=student)

    def get_pending_ticket_for(self, student: User) -> Optional[Ticket]:
        """
        Get a pending ticket for a certain student on this queue.
        (There should only be one pending ticket).
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        The pending ticket of the student on this queue.\n
        """
        return Ticket.find_all_tickets_by_student(queue=self, student=student,
                                                  status=[t_status.PENDING])[0]

    def get_accepted_ticket_for(self, student: User) -> Optional[Ticket]:
        """
        Get an accepted ticket for a certain student on this queue.
        (There should only be one pending ticket).
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        The pending ticket of the student on this queue.\n
        """
        return Ticket.\
            find_all_tickets_by_student(queue=self, student=student,
                                        status=[t_status.ACCEPTED])[0]

    def get_unresolved_ticket_for(self, student: User) -> Optional[Ticket]:
        """
        Get an unresolved ticket for a certain student on this queue.
        (There should only be one pending ticket).
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        The pending ticket of the student on this queue.\n
        """
        return Ticket.find_all_tickets_by_student(queue=self, student=student,
                                                  status=[t_status.ACCEPTED,
                                                          t_status.PENDING])[0]

    def get_resolved_ticket_for(self, student: User) -> List[Ticket]:
        """
        Get an resolved ticket for a certain student on this queue.
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        A list of tickets of the student on this queue that are resolved.\n
        """
        return Ticket.find_all_tickets_by_student(queue=self, student=student,
                                                  status=[t_status.RESOLVED])

    def get_canceled_ticket_for(self, student: User) -> List[Ticket]:
        """
        Get an canceled ticket for a certain student on this queue.
        Inputs:\n
        student -> The User object for the student.\n
        Returns:\n
        A list of tickets of the student on this queue that are resolved.\n
        """
        return Ticket.find_all_tickets_by_student(queue=self, student=student,
                                                  status=[t_status.CANCELED])

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
            -> List[Ticket]:
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
        if all:
            return Ticket.find_all_ticket_accpeted_by_grader(self,
                                                             grader=grader)
        else:
            return [Ticket.find_ticket_accpeted_by_grader(self, grader=grader)]

    def get_ticket_resolved_by(self, grader: User) -> List[Ticket]:
        """
        Get all the tickes resolved by a grader.
        Inputs:\n
        grader --> The grader to search for.\n
        Returns:\n
        A list of tickest that is resolved by the grader.\n
        """
        tickets = Ticket.find_all_tickets_for_grader(self, grader)
        return list(filter(lambda x: x.status == t_status.RESOLVED), tickets)

    # Grader tickets bool query methods
    def has_ticket_accepted_by(self, grader: User) -> bool:
        return len(self.get_ticket_accepted_by(grader)) != 0

    # News feed post functionalities
    def get_news_feed_post(self, num: int = 20) -> List[NewsFeedPost]:
        """
        Get the news feed post on the queue.
        Inputs:\n
        num --> The number of news feed posts to look up for.
        Returns:\n
        A list of news feed post.
        """
        # return nfp.find...
        # Use the npf.find methods for the news_feed_post
        pass

    def get_archived_news_feed_post(self, num: int = 20)\
            -> List[NewsFeedPost]:
        """
        Get the archeived news feed posts for the queue.
        Inputs:\n
        Inputs:\n
        num --> The number of news feed posts to look up for.
        Returns:\n
        A list of archived news feed post.
        """
        # return nfp.find...
        # Use the npf.find methods for the news_feed_post
        pass

    # Impelementing Queue Stats
    def average_help_time(self, day: bool = True, hour: bool = False,
                          start: datetime = None,
                          end: datetime = None) -> timedelta:
        """
        Get the average help time within a time period for tickes in
        the queue.\n
        Inputs:\n
        day --> To look for a day, default would be true.\n
        hour --> To look for the recent hour, default would be false.\n
        start --> The start time to look for. The default would be None.
                  If start is provided, it has priority among hour and day.\n
        end --> The end time to look for. The default would be None.
                end would only work if start is provied.\n
        Returns:\n
        A timedelta object representing the averge help time for the tickes
        given that period.\n
        """
        if not start:
            day = False
            hour = False
        tickets = Ticket.find_resolved_tickets_in(self, day=day,
                                                  hour=hour,
                                                  start=start, end=end)
        if len(tickets) < 5:
            return MIN_WAIT_TIME
        average_resolved_time = Ticket.average_resolved_time(tickets)
        return timedelta(seconds=average_resolved_time)

    # getExpectedTimeUntilAvailableTutor need a query method probably in
    # enrolled classs...
    def wait_time_for_next_tutor(self) -> timedelta:
        """
        Get the expected wait time for the next tutor to be avaliable
        Returns:\n
        The timedelta object for the expected time for the next tutor to be
        avaliale.
        """
        ave_resolve_time = self.average_help_time(hour=True)
        # pending_num = self.get_pending_tickets()
        active_tutor_num = EnrolledCourse.find_active_tutor_for(self)  # need ec
        # Use enrolled course methods to find the num of active tutor.
        accepted_tickets = self.get_accepted_tickets()
        next_avaliable = timedelta(seconds=0)
        if active_tutor_num > len(accepted_tickets):
            return next_avaliable
        now = datetime.now()
        # Simplifing the algorithm for now (without using utils)
        for ticket in accepted_tickets:
            current_help_time = now - ticket.accepted_at
            potential_time_need = ave_resolve_time - current_help_time
            next_avaliable = max(next_avaliable, potential_time_need)

        return next_avaliable

    def get_wait_time(self, student: User) -> Optional[timedelta]:
        """
        Get the expected wait time for a student.\n
        Inputs:\n
        The student User object.\n
        Returns:\n
        The expected wait time for this student's ticket to be accepted.
        If this student has no tickect in the queue, return None.\n
        """
        student_ticket = self.get_pending_ticket_for(student=student)
        if student_ticket is None:
            return None
        # Get the number of tickets before this student's
        position = student_ticket.get_position()
        wait_time = timedelta(seconds=0)
        next_avaliable = self.wait_time_for_next_tutor()
        ave_help_time = self.average_help_time()
        wait_time = position * ave_help_time + next_avaliable

        return wait_time

    def get_queue_wait_time(self) -> timedelta:
        """
        Given all the tickets in the queue, calculate the expected wait time
        if a ticket is submited now.\n
        Return:\n
        The expected wait time for a ticket that is submited now.\n
        """
        pending_num = len(self.get_pending_tickets())
        ave_time = self.average_help_time()

        return pending_num * ave_time

    # Static add method
    @staticmethod
    def add_to_db(queue: Queue):
        """
        Add the queue feedback to the database.\n
        Inputs:\n
        queue --> the queue object created.\n
        """
        db.session.add(queue)
        db.session.commit()

    @staticmethod
    def create_queue():
        """
        Create a new queue to the database.\n
        """
        queue = Queue()
        Queue.add_to_db(queue)

    @staticmethod
    def get_queue_by_id(queue_id: id) -> Optional(Queue):
        """
        Find the queue by the queue_id.\n
        Inputs:\n
        queue_id --> The id of the queue to look for.\n
        Returns:\n
        The queue object, return None if it is not in the database.\n
        """
        return Queue.query().filter(id=queue_id).first()

    # None Memeber Queue Methods
    @staticmethod
    def grader_login(queue_id: int, grader_id: int,
                     action_type: ActionType =
                     ActionType.MANUAL) -> bool:
        """
        Login a grader when the grader login to he queue.\n
        Inputs:\n
        queue --> The queue that the grader is logging in.\n
        grader --> The grader that is logging in.\n
        action_type --> The type of action for logging in, default MANUAL.\n
        Return:\n
        True or false indicates whether the function is successful.
        """
        queue = Queue.get_queue_by_id(queue_id)
        if not queue:
            return False
        course = Course.find_course_by_queue(queue_id)
        if not course:
            return False
        grader = User.get_user_by_id(grader_id)
        if not grader:
            return False
        grader.change_status(course, User.Status.AVALIABLE)
        event = QueueLoginEvent(event_type=EventType.LOGIN,
                                action_type=action_type,
                                grader_id=grader_id,
                                queue_id=queue_id
                                )
        QueueLoginEvent.add_to_db(event)
        queue.open()
        return True

    @staticmethod
    def grader_logout(queue_id: int, grader_id: int,
                      action_type: ActionType) -> bool:
        """
        Logout a grader when the grader logout from queue.\n
        Inputs:\n
        queue --> The queue that the grader is logging out.\n
        grader --> The grader that is logging out.\n
        action_type --> The type of action for logging out.\n
        Return:\n
        True or false indicates whether it the function runs successfully.
        """
        queue = Queue.get_queue_by_id(queue_id)
        if not queue:
            return False
        grader = User.get_user_by_id(grader_id)
        if not grader:
            return False
        course = Course.find_course_by_queue(queue)  # Prentending
        if not course:
            return False
        grader.change_status(course, User.Status.AVALIABLE)
        event = QueueLoginEvent(event_type=EventType.LOGOUT,
                                action_type=action_type,
                                grader_id=grader.id,
                                queue_id=queue.id
                                )
        QueueLoginEvent.add_to_db(event)
        queue.open()
        return True

    @staticmethod
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
        # the enrolled classes of that user and fetch the queues of class.
        pass

    @staticmethod
    def find_queue_for_course(course: Course) -> Optional[Queue]:
        """
        Find the queue corresponding for a course.
        Inputs:\n
        course --> the Course object to look for.
        Returns:\n
        The queue for that course, if a queue does not exist, None is return.\n
        """
        return Queue.query().filter(id=course.queue_id).first()
