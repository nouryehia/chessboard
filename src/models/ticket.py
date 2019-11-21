from app import db
from enum import Enum
from typing import List
from ticket_tag import Types
from datetime import datetime


# Only 3 tags allowed per ticket
MAX_TAG_NUM = 3


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
    Question = 0
    Checkoff = 1


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
    status = db.Column(db.Integer(11), nullable=False)
    created_at = db.Column(db.DateTime, nullabble=True)
    closed_at = db.Column(db.DateTime, nullabble=True)
    room = db.Column(db.String(255), nullable=False)
    workstaton = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer(11), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    grader_id = db.Column(db.Integer(20), db.ForeignKey('user.id'),
                          nullable=True)
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

    def update(self, title: str, description: str, room: str,
               workstation: str, isPrivate: bool, help_type: HelpType,
               tag_list: List[Types]) -> None:
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
        self.title = title
        self.description = description
        self.room = room
        self.workstation = workstation
        self.isPrivate = isPrivate
        self.help_type = help_type

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

        # Do I need to commit to the database here or no?

    def get_help_time_in_second(self) -> float:
        """
        Get the time in second of the time that this ticket spent\
        to be resolved.\n
        Return:\n
        The difference in time.\n
        """
        return (self.closed_at - self.created_at).total_second()

    def second_to_minute(self, second: float) -> float:
        """
        Convert to minute from second.\n
        Return:\n
        The second in float format.\n
        """
        return second / 60
