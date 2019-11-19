from app import db
from enum import Enum
# from datetime import datetime


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
