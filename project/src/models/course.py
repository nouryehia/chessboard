# from typing import Optional, List
from ...setup import db
from enum import Enum
#from .enrolled_course import EnrolledCourse
# from . import  Section
from typing import Optional


class Role(Enum):
    """
    All the roles that a user can have for a class.\n
    The following fields are difend as name --> database value:\n
    Fields --> Database Value:\n
    ROOT --> 0\n
    ADMIN --> 1\n
    INSTRUCTOR --> 2\n
    GRADER --> 3\n
    STUDENT --> 4\n
    @author: YixuanZhou
    """
    ROOT = 0
    ADMIN = 1
    INSTRUCTOR = 2
    GRADER = 3
    STUDENT = 4


class Quarter(Enum):
    """
    Enum for quarters.
    Fields --> Database Value:\n
    FALL --> 0\n
    WINTER --> 1\n
    SPRING --> 2\n
    SS1 --> 3\n
    SS2 --> 4\n
    @author: mihaivaduva21 
    """
    FALL = 0
    WINTER = 1
    SPRING = 2
    SS1 = 3
    SS2 = 4


class Course(db.Model):
    """
    Represents a course in the DB with relevant functions for
    manipulation of course data.
    Fields:
    id --> Course ID. Unique, primary key
    description --> Description of text
    name --> Name of the course
    quarter --> The quarter in which the course is held
    short_name --> Shortened name of the course
    year --> Year in which the course is held
    active --> boolean representing if the course is currently held.
    queue_enabled --> boolean representing if the queue is enabled or not.
    cse --> True if CSE course false otherwise
    lock_button --> true if queue enabled, false otherwise
    queue_id -->  Queue id, unique referencing Queue table
    @author:Mihai
    """
    __tablename__ = 'Course'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    quarter = db.Column(db.Integer, nullable=False)
    short_name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    queue_enabled = db.Column(db.Boolean, nullable=False, default=False)
    cse = db.Column(db.Boolean, nullable=False, default=True)
    lock_button = db.Column(db.Boolean, nullable=False, default=False)
    queue_id = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        """
        The constructor of the queue calendar object.\n
        """
        super(Course, self).__init__(**kwargs)

    def save(self):
        """
        Save the object in the database.
        """
        db.session.commit()

    def __repr__(self) -> str:
        """
        repr
        """
        return (str)(self.id, self.name, self.short_name, self.quarter,
                     self.year)

    def switch_queue_status(self):
        """
        Switches the status of the queue.
        """
        self.queue_enabled = not (self.queue_enabled)
        self.save()

    def switch_lock_status(self):
        """
        Switches the status of the lock.
        """
        self.lock_button = not (self.lock_button)
        self.save()

    def switch_active_status(self):
        """
        Switches the active status
        """
        self.active = not(self.active)
        self.save()

    def switch_cse(self):
        """
        Switch the value of the cse boolean
        """
        self.cse = not(self.cse)
        self.save()

    def get_sections(self):
        """
        Get the sections of a course
        """
        return Section.query.filter_by(course_id=self.id).all()

    '''
    def get_students(self):
        """
        Get the students enrolled in a course
        """
        sections = Section.query.with_entities(Section.id).filter_by(course_id=self.id).all()
        students = []
        for section in sections:
            students = students + EnrolledCourse.query.filter_by(section_id=section, role=Role.STUDENT.value).all()

        return students

    
    def get_instructors(self):
        """
        Get the instructors from a course
        """
        sections = Section.query.with_entities(Section.id).filter_by(course_id=self.id).all()
        instructors = []
        for section in sections:
            instructors = instructors + EnrolledCourse.query.filter_by(section_id=section, role=Role.INSTRUCTOR.value).all()

        return instructors
    '''

    def get_course_by_queue_id(self, q_id):
        """
        Returns a Course from a course id
        """
        course = Course.query.filter_by(queue_id=q_id).first()
        return course

    def quarter_year(self):
        """
        Returns the quarter and the year.
        """
        if self.quarter is Quarter.FALL:
            return "FA" + str(self.year)
        elif self.quarter is Quarter.WINTER:
            return "WI" + str(self.year)
        elif self.quarter is Quarter.SPRING:
            return "SP" + str(self.year)
        elif self.quarter is Quarter.SS1:
            return "SS1" + str(self.year)
        elif self.quarter is Quarter.SS2:
            return "SS2" + str(self.year)

    '''
    def add_section(self, section_name):
        """
        Adds a section to the course.
        """
        Section.insert().values(section_name=section_name, course_id=self.id)
    '''

    def exists_course(quarter: int, short_name: str, year: int):
        '''
        Function that tries to find a course by short name, quarter and year.

        Params: pid - string. email - string.\n
        Returns: Optional[Course] or None
        '''
        try:
            user = Course.query.filter_by(quarter=quarter,
                                          short_name=short_name,
                                          year=year).first()
        except KeyError:
            user = None

        return user

    @staticmethod
    def create_course(description: str, name: str, quarter: int,
                      short_name: str, url: str, year: int,
                      active: bool, queue_enabled: bool, cse: bool,
                      queue_id: int):

        """
        Creates a new course and adds it to the databease.
        """
        if Course.exists_course(quarter, short_name, year) is not None:
            return None

        course = Course(description=description, name=name, quarter=quarter,
                        short_name=short_name, url=url, year=year,
                        active=active, queue_enabled=queue_enabled, cse=cse,
                        lock_button=False, queue_id=queue_id)
        db.session.add(course)
        db.session.commit()
        return course


    @staticmethod
    def delete_course(short_name: str, quarter: int, year: int) -> bool:
        """
        Delete an entry from the enrolled_course table.\n
        Inputs:\n
        user_id --> The user_id of the user to delete.\n
        course_id --> The course_id of the course to delete user from.\n
        """
        enrolled_user = Course.exists_course(quarter, short_name, year)
        if enrolled_user:
            db.session.delete(enrolled_user)
            db.session.commit()
            return True
        else:
            return False
