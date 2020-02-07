# from typing import Optional, List
from datetime import datetime , date
from app import db
from .models import Users, Section, EnrolledCourse


# we will probably need more roles
INSTRUCTOR_ROLE = 1
STUDENT_ROLE = 2
GRADER_ROLE = 3

FALL = 0
WINTER = 1
SPRING = 2
SS1 = 3
SS2 = 4

fa_begin  = date(datetime.date.today().year,9,20)
wi_begin  = date(datetime.date.today().year,1,1)
sp_begin  = date(datetime.date.today().year,3,20)
ss1_begin = date(datetime.date.today().year)
ss2_begin = date(datetime.date.today().year)





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
    year = db.Column(db.Integer, nullable=False)
    queue_enabled = db.Column(db.Boolean, nullable=False, default=False)
    cse = db.Column(db.Boolean, nullable=False, default=True)
    lock_button = db.Column(db.Boolean, nullable=False, default=False)
    queue_id = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
   
    def __init__(self, id, name, short_name, description, quarter, year): 
        self.id = id
        self.name = name
        self.short_name = short_name
        self.description = description
        self.quarter = quarter
        self.year = year
        self.save()

    def save(self) -> None:
        db.session.commit()

    def switchQueueStatus(self):
        self.queue_enabled = not (self.queue_enabled)
        self.save()

    def switchLockStatus(self):
        self.lock_button = not (self.lock_button)
        self.save()

    def switchActiveStatus(self):
        self.active = not(self.active)
        self.save()

    def switchCSE(self):
        self.cse = not(self.cse)
        self.save()

    def getSections(self):
        return Section.query.filter_by(course_id=self.id).all()
    
    def getStudents(self):
        sections = Section.query.with_entities(Section.id).filter_by(course_id=self.id).all()
        students = []
        for section in sections:
            students += EnrolledCourse.query.filter_by(section_id=section, role=STUDENT_ROLE).all()

        return students

    def getInstructors(self):
        sections = Section.query.with_entities(Section.id).filter_by(course_id=self.id).all()
        instructors = []
        for section in sections:
            instructors += EnrolledCourse.query.filter_by(section_id=section, role=INSTRUCTOR_ROLE).all()

        return instructors

    def getCourseByQueueID(self, q_id):
        course = Course.query.filter_by(queue_id=q_id).first()
        return course

    def quarterYear(self):
        if self.quarter is FALL:
            return "FA" + str(self.year)
        elif self.quarter is WINTER:
            return "WI" + str(self.year)
        elif self.quarter is SPRING:
            return "SP" + str(self.year)
        elif self.quarter is SS1:
            return "SS1" + str(self.year)
        elif self.quarter is SS2:
            return "SS2" + str(self.year)

    def toString(self):
        return self.short_name

    def addSection(self, section_name):
        Section.insert().values(section_name=section_name, course_id=self.id)

    def getCurrentQuarter():
        
        today = date.today()
