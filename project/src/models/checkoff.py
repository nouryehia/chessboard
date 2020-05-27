from __future__ import annotations

from ...setup import db
from typing import List, Optional
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
        checkoff.suite_id = self.id
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
        checkoffs = Checkoff.find_all_checkoffs_for_suite(self.id)
        for checkoff in checkoffs:
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
        checkoffs = Checkoff.find_all_checkoffs_for_suite(self.id)
        for checkoff in checkoffs:
            if (CheckoffEvaluation.find_checkoff(checkoff.id, student_id)
                    is not None):
                total += 1
        return total

    def get_newest_checkoff_eval_for_student(self, student_id: int) -> None:
        """
        Returns newest checkoff that was evaluated for the student\n
        Params:\n
        student_id --> student to find checkoff for\n
        Return:\n
        Last checkoff that was evaluated for the student\n
        """
        last_checkoff_evaluation = None
        checkoffs = Checkoff.find_all_checkoffs_for_suite(self.id)
        for checkoff in checkoffs:
            checkoff_evaluation = CheckoffEvaluation \
                                  .find_newest_checkoff(checkoff.id,
                                                        student_id)
            if checkoff_evaluation:
                if last_checkoff_evaluation:
                    last_checkoff_evaluation = checkoff_evaluation
                elif (last_checkoff_evaluation.checkoff_time ==
                        checkoff_evaluation.checkoff_time) < 0:
                    last_checkoff_evaluation = checkoff_evaluation
        return last_checkoff_evaluation

    @staticmethod
    def create_suite(status: int) -> CheckoffSuite:
        cs = CheckoffSuite(status=status)
        db.session.add(cs)
        db.session.commit()

        return cs

    @staticmethod
    def find_by_id(checkoff_id: int) -> Optional[CheckoffSuite]:
        """
        Finds a CheckoffSuite by its id in the database\n
        Params: \n
        checkoff_id --> id of the CheckoffSuite\n
        Return:\n
        CheckoffSuite corresponding to that id\n
        """
        return CheckoffSuite.query.filter_by(
            id=checkoff_id, is_deleted=False).first()


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
    suite_id = db.Column(db.Integer, db.ForeignKey(CheckoffSuite.id),
                         nullable=False)
    points = db.Column(db.Integer(11), nullable=False)

    @staticmethod
    def create_checkoff(description: str, name: str, suite_id: int,
                        points: int) -> Checkoff:
        '''
        Creates a new checkoff in the database\n
        Params:\n
        description --> Description of the checkoff\n
        name --> Name of the checkoff\n
        suite_id --> ID of checkoff's CheckoffSuite\n
        points --> Points the checkoff is worth\n
        Return:\n
        Checkoff that was created in the database
        author @sravyabalasa
        '''
        c = Checkoff(description=description, name=name, suite_id=suite_id,
                     points=points)
        db.session.add(c)
        db.session.commit()

        return c

    @staticmethod
    def find_all_checkoffs_in_suite(suite_id: int) -> Optional[List[Checkoff]]:
        """
        Returns all checkoffs with this checkoff suite ID
        Fields:
        suite --> ID of the Checkoff Suite
        Return:
        List of Checkoffs in the same CheckoffSuite
        @author sravyabalasa
        """
        return CheckoffSuite.query.filter_by(suite_id=suite_id).all()


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
    def create_eval(checkoff_id: int, grader_id: int,
                    student_id: int) -> CheckoffEvaluation:
        '''
        TIME UTIL THINGS
        '''
        """
        Creates a new checkoff evaluation\n
        Params:\n
        checkoff --> id of checkoff\n
        grader --> id of grader for checkoff\n
        student --> id of student\n
        Return:\n
        A new checkoff evaluation\n
        """
        ce = CheckoffEvaluation(checkoff_id=checkoff_id, grader_id=grader_id,
                                student_id=student_id)
        db.session.add(ce)
        db.session.commit()

        return ce

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
            .order_by(CheckoffEvaluation.checkoff_time).desc().first()
