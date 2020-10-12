from __future__ import annotations

from ...setup import db
from typing import List, Optional
from .user import User
from .enrolled_course import EnrolledCourse
from enum import Enum
from ..utils.time import TimeUtil


class Status(Enum):
    """
    Enum that describes the different statuses a checkoff can be at\n
    it its lifecycle\n
    """
    HIDDEN = 0          # Created but not available to students/graders
    AVAILABLE = 1       # Available to students for submission
    FINALIZED = 2       # Grades submitted, moved to archived state


class Checkoff(db.Model):
    """
    Represents a checkoff in the DB with relevant description and points.\n
    Fields:\n
    id --> Checkoff ID. Unique, primary key\n
    due --> When checkoff is due\n
    description --> Description of checkoff\n
    name --> Corresponding assignment\n
    course_id --> ID of course checkoff is in\n
    points --> Number of points checkoff is worth\n
    status --> Checkoff availability status\n
    is_deleted --> Whether checkoff is deleted or not\n
    @author sravyabalasa
    """
    __tablename__ = 'Checkoff'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    due = db.Column(db.DateTime, nullable=True, default=TimeUtil.get_current_time())
    description = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)

    def save(self):
        '''
        Saves the current object in the DB.\n
        Params: None\n
        Returns: None\n
        '''
        db.session.commit()

    def to_json(self):
        '''
        Function that takes a checkoff object and returns it in a dictionary
        form. Used on the API layer.\n
        Params: None\n
        Returns: Dictionary of the checkoff object
        '''
        ret = {}
        ret['id'] = self.id
        ret['description'] = self.description
        ret['name'] = self.name
        ret['course_id'] = self.course_id
        ret['points'] = self.points
        ret['status'] = self.status
        ret['due'] = self.due
        ret['is_deleted'] = self.is_deleted
        return ret

    def set_hidden(self) -> None:
        """
        Sets the checkoff to hidden\n
        Params: None\n
        Return: None\n
        """
        self.status = Status.HIDDEN.value
        self.save()

    def set_available(self) -> None:
        """
        Sets the checkoff to available\n
        Params: None\n
        Return: None\n
        """
        self.status = Status.AVAILABLE.value
        self.save()

    def set_finalized(self) -> None:
        """
        Sets the checkoff to finalized\n
        Params: None\n
        Return: None\n
        """
        self.status = Status.FINALIZED.value
        self.save()

    def soft_delete(self) -> None:
        '''
        Sets the checkoff to deleted and returns this checkoff.\n
        Params: None\n
        Returns: This assignment.
        '''
        self.is_deleted = True
        self.save()
        return self

    def update_checkoff(self, description: str, name: str, points: int, due: str) -> Checkoff:
        '''
        Updates a checkoff based on information entered by user\n
        Params:\n
        description --> Description of the checkoff\n
        name --> Name of the checkoff\n
        points --> Points the checkoff is worth\n
        '''
        self.description = description
        self.name = name
        self.points = points
        self.due = TimeUtil.convert_str_to_datetime(due)

        #TODO: Update the checkoff evaluations as well?? With updated score if points change??
        self.save()

    @staticmethod
    def get_checkoff_by_id(checkoff_id: int) -> Checkoff:
        '''
        Returns a checkoff based on the id associated with it
        Params:\n
        checkoff_id --> ID of checkoff to query for\n
        Return:\n
        Checkoff corresponding to ID passed in
        '''
        #TODO: Delete checkoff that deletes all the checkoff evalutations? query by is_deleted for both?
        return Checkoff.query.filter_by(id=checkoff_id).first()

    @staticmethod
    def create_checkoff(description: str, name: str, course_id: int,
                        points: int, due: str) -> Checkoff:
        '''
        Creates a new checkoff in the database\n
        Params:\n
        description --> Description of the checkoff\n
        name --> Name of the checkoff\n
        course_id --> ID of course checkoff belongs to\n
        points --> Points the checkoff is worth\n
        due --> When the checkoff is due\n
        Return:\n
        Checkoff that was created in the database
        author @sravyabalasa
        '''
        c = Checkoff(description=description, name=name, course_id=course_id,
                     points=points, is_deleted=False, status=Status.HIDDEN.value, due=TimeUtil.convert_str_to_datetime(due))
        db.session.add(c)
        c.save()

        return c

    @staticmethod
    def find_all_checkoffs_in_course(course_id: int) -> List[Checkoff]:
        """
        Returns all checkoffs in the course
        Fields:
        course_id --> ID of the course
        Return:
        List of Checkoffs in the course
        @author sravyabalasa
        """
        return Checkoff.query.filter(course_id=course_id, is_deleted=False).all()


class CheckoffEvaluation(db.Model):
    """
    Represents individual checkoff status for each indiviudal.\n
    Allows graders to checkoff students and evaluate their performance\n
    Fields:
    id --> User ID. Unique, primary key\n
    checkoff_time --> Time of checkoff evaluation by grader
    checkoff_id --> Foreign Key to corresponding Checkoff\n
    grader_id --> Foreign Key to grader's user\n
    student_id --> Foreign Key to student's user\n
    score --> Number of points awarded to student\n
    @author sravyabalasa
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    checkoff_time = db.Column(db.DateTime, nullable=True,
                              default=TimeUtil.get_current_time())
    checkoff_id = db.Column(db.Integer, db.ForeignKey('Checkoff.id'),
                            nullable=False)
    grader_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                          nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                           nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def save():
        '''
        Saves the current object in the DB.\n
        Params: None\n
        Returns: None\n
        '''
        db.session.commit()

    @staticmethod
    def create_eval(checkoff_id: int, grader_id: int,
                    student_id: int, score_fract: float) -> CheckoffEvaluation:
        """
        Creates a new checkoff evaluation\n
        Params:\n
        checkoff --> id of checkoff\n
        grader --> id of grader for checkoff\n
        student --> id of student\n
        score_fract --> how much of the score they got (full, 1/2, none)
        Return:\n
        A new checkoff evaluation\n
        """
        checkoff = Checkoff.get_checkoff_by_id(checkoff_id)
        score = checkoff.points * score_fract

        ce = CheckoffEvaluation(checkoff_id=checkoff_id, grader_id=grader_id,
                                student_id=student_id, score=score)
        db.session.add(ce)
        ce.save()

        return ce

    @staticmethod
    def find_latest_ce_for_checkoff_for_all_students(course_id: int, checkoff_id: int) -> List[Tuple[User,CheckoffEvaluation]]:
        '''
        Finds latest checkoff evaluation for each student in a course
        Params:\n
        course_id --> ID of course to get students' checkoffs for\n
        checkoff_id --> ID of checkoff to get latest evalution for\n
        Return:\n
        A list of tuples of Users, CheckoffEvaluations
        '''
        students = EnrolledCourse.find_all_user_in_course(course_id, 4)

        ce_map = []
        for student in students:
            ce = CheckoffEvaluation.find_latest_ce_for_checkoff_for_student(checkoff_id, student.id)
            ce_map.append(student, ce)
        return ce_map

    @staticmethod
    def find_latest_ce_for_all_checkoffs_for_student(course_id: int, student_id: int) -> List[CheckoffEvaluation]:
        """
        Finds latest checkoff evaluations for checkoffs in course for student
        Params:\n
        course_id --> ID of the course to find CheckoffEvaluations for\n
        student_id --> ID of the student\n
        Return:\n
        A list of CheckoffEvaluations for the student
        """
        checkoffs = Checkoff.find_all_checkoffs_in_course(course_id)

        latest_ce = []
        for checkoff in checkoffs:
            latest_ce.append(CheckoffEvaluation.find_latest_ce_for_checkoff_for_student(checkoff.id, student_id))

        return latest_ce

    @staticmethod
    def find_latest_ce_for_checkoff_for_student(checkoff_id: int,
                                                student_id: int) -> Optional[CheckoffEvaluation]:
        """
        Finds checkoff evaluated for the student\n
        Params:\n
        checkoff_id --> ID of the checkoff assignment\n
        student_id --> ID of the student\n
        Return:\n
        A CheckoffEvaluation for the student\n
        """
        return CheckoffEvaluation.query \
            .filter_by(checkoff_id=checkoff_id,
                       student_id=student_id).order_by(CheckoffEvaluation.checkoff_time.desc()).first()
