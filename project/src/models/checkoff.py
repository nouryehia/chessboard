from __future__ import annotations

from ...setup import db
from typing import List, Optional
from .assignment import Assignment
from .user import User
from enum import Enum


class Status(Enum):
    """
    Enum that describes the different statuses a checkoff can be at\n
    it its lifecycle\n
    """
    HIDDEN = 0          # Created but not available to students/graders
    AVAILABLE = 1       # Available to students for submission
    FINALIZED = 2       # Grades submitted, moved to archived state


class CheckoffSuite(db.Model):
    """
    Represents the readiness state of Checkoff in the Assignment lifecycle.\n
    Independent of the state of individual submissions\n
    Fields:\n
    id --> CheckoffSuite ID. Unique, primary key\n
    status --> Checkoff availability status \n
    @author sravyabalasa
    """
    __tablename__ = 'CheckoffSuite'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer(11), nullable=False)

    def __init__(self,
                 assignment: Assignment,
                 checkoffs: List[Checkoff], **kwargs):
        """
        Constructor that adds extra non-database fields for a checkoff\n
        suite\n
        """
        super(CheckoffSuite, self).__init__(**kwargs)
        self.assignment = assignment
        self.checkoffs = checkoffs

    def is_hidden(self) -> bool:
        """
        Returns if the checkoff is hidden\n
        Params: None\n
        Return:\n
        Bool indicating if the checkoff is hidden\n
        """
        return self.status == Status.HIDDEN

    def is_available(self) -> bool:
        """
        Returns if the checkoff is available\n
        Params: None\n
        Return:\n
        Bool indicating if the checkoff is available\n
        """
        return self.status == Status.AVAILABLE

    def is_finalized(self) -> bool:
        """
        Returns if the checkoff is finalized\n
        Params: None\n
        Return:\n
        Bool indicating if the checkoff is finalized\n
        """
        return self.status == Status.FINALIZED

    def set_hidden(self) -> None:
        """
        Sets the checkoff to hidden\n
        Params: None\n
        Return: None\n
        """
        self.status = Status.HIDDEN
        db.session.commit()

    def set_available(self) -> None:
        """
        Sets the checkoff to available\n
        Params: None\n
        Return: None\n
        """
        self.status = Status.AVAILABLE
        db.session.commit()

    def set_finalized(self) -> None:
        """
        Sets the checkoff to finalized\n
        Params: None\n
        Return: None\n
        """
        self.status = Status.FINALIZED
        db.session.commit()

    def add_checkoff(self, checkoff: Checkoff) -> None:
        """
        Adds a new checkoff to the suite\n
        Params:\n
        checkoff --> checkoff to add to the suite\n
        Return: None\n
        """
        self.checkoffs.add(checkoff)
        db.session.commit()

    def find_by_id(self, checkoff_id: int) -> Optional[CheckoffSuite]:
        """
        Finds a CheckoffSuite by its id in the database\n
        Params: \n
        checkoff_id --> id of the checkoffSuite\n
        Return:\n
        CheckoffSuite corresponding to that id\n
        """
        return CheckoffSuite.query.filter_by(
            id=checkoff_id, is_deleted=False).first()

    def get_max_score(self) -> int:
        """
        Sums up the scores off all the checkoffs in suite\n
        Params:\n
        Return: Sum of all scores in the suite\n
        """
        total = 0
        for checkoff in self.checkoffs:
            total += checkoff.points
        return total

    def get_score_for_student(self, student_id: int) -> int:
        """
        Returns the student's checkoff score in this suite\n
        Params:\n
        student_id --> student to find checkoff for\n
        Return:\n
        Student's score in the checkoff suite\n
        """
        total = 0
        for checkoff in self.checkoffs:
            if CheckoffEvaluation.find_checkoff(checkoff.id, student_id):
                total += 1
        return total

    def get_newest_checkoff_evaluation_for_student(self,
                                                   student_id: int) -> None:
        """
        Returns newest checkoff that was evaluated for the student\n
        Params:\n
        student_id --> student to find checkoff for\n
        Return:\n
        Last checkoff that was evaluated for the student\n
        """
        last_checkoff_evaluation = None
        for checkoff in self.checkoffs:
            checkoff_evaluation = CheckoffEvaluation \
                                  .find_newest_checkoff(checkoff.id, student_id)
            if checkoff_evaluation:
                if last_checkoff_evaluation:
                    last_checkoff_evaluation = checkoff_evaluation
                elif (last_checkoff_evaluation.checkoff_time ==
                        checkoff_evaluation.checkoff_time) < 0:
                    last_checkoff_evaluation = checkoff_evaluation
        return last_checkoff_evaluation


class Checkoff(db.Model):
    """
    Represents a checkoff in the DB with relevant description and points.\n
    Fields:\n
    id --> Checkoff ID. Unique, primary key\n
    description --> Description of checkoff\n
    name --> Corresponding assignment\n
    suite_id --> ID of assignment checkoff is for\n
    points --> Number of points checkoff is worth\n
    @author sravyabalasa
    """
    __tablename__ = 'Checkoff'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    suite_id = db.Column(db.Integer(11), nullable=False)
    points = db.Column(db.Integer, db.ForeignKey(CheckoffSuite.id),
                       nullable=False, default=1)


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
    @author sravyabalasa
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    checkoff_time = db.Column(db.DateTime, nullable=False)
    checkoff_id = db.Column(db.Integer, db.ForeignKey(Checkoff.id),
                            nullable=False)
    grader_id = db.Column(db.Integer, db.ForeignKey(User.id),
                          nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(User.id),
                           nullable=False)

    @staticmethod
    def create_eval(assignment: Checkoff, grader: User,
                    student: User) -> CheckoffEvaluation:
        """
        Creates a new checkoff evaluation\n
        Params:\n
        assignment --> Checkoff assignment\n
        grader --> Grader for the checkoff\n
        student --> User who the checkoff belongs to\n
        Return:\n
        A new checkoff evaluation\n
        """
        return CheckoffEvaluation(assignment, grader, student)

    @staticmethod
    def find_checkoff(checkoff_id: int,
                      student_id: int) -> Optional[CheckoffEvaluation]:
        """
        Finds checkoff evaluated for the student\n
        Params:\n
        checkoff_id --> ID of the checkoff assignment\n
        student_id --> ID of the student\n
        Return:\n
        A checkoff evauluation for the student\n
        """
        return CheckoffEvaluation.query \
            .filter_by(checkoff_id=checkoff_id,
                       student_id=student_id).first()

    def find_newest_checkoff(self, checkoff_id: int,
                             student_id: int) -> Optional[CheckoffEvaluation]:
        """
        Find the newest checkoff evaluated for the student\n
        Params:\n
        checkoff_id --> ID of the checkoff\n
        student_id --> ID of the student\n
        Return:\n
        Newest checkoff evaluation for the student\n
        """
        return CheckoffEvaluation.query \
            .filter_by(checkoff_id=checkoff_id, student_id=student_id) \
            .order_by(self.checkoff_time).desc().first()
