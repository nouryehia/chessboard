from app import db
from typing import List
from checkoff_evaluation import CheckoffEvaluation
from checkoff_suite import Checkoff
from assignment import Assignment
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
    Fields:
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

        Params: None

        Return:\n
        Bool indicating if the checkoff is hidden
        """
        return self.status == Status.HIDDEN

    def is_available(self) -> bool:
        """
        Returns if the checkoff is available\n
        Params: None\n
        Return:\n
        Bool indicating if the checkoff is available
        """
        return self.status == Status.AVAILABLE

    def is_finalized(self) -> bool:
        """
        Returns if the checkoff is finalized\n
        Params: None\n
        Return:\n
        Bool indicating if the checkoff is finalized
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
        checkoff --> checkoff to add to the suite
        Return: None\n
        """
        self.checkoffs.add(checkoff)
        db.session.commit()

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
        Student's score in the checkoff suite
        """
        total = 0
        for checkoff in self.checkoffs:
            if (CheckoffEvaluation.findCheckoff(checkoff.id, student_id)
                    is not None):
                total += 1
        return total

    def get_newest_checkoff_evaluation_for_student(self,
                                                   student_id: int) -> None:
        """
        Returns newest checkoff that was evaluated for the student\n
        Params:\n
        student_id --> student to find checkoff for\n
        Return:\n
        Last checkoff that was evaluated for the student
        """
        last_checkoff_evaluation = None
        for checkoff in self.checkoffs:
            checkoff_evaluation = CheckoffEvaluation \
                                  .findNewestCheckoff(checkoff.id, student_id)
            if checkoff_evaluation is not None:
                if last_checkoff_evaluation is None:
                    last_checkoff_evaluation = checkoff_evaluation
                elif (last_checkoff_evaluation.checkoff_time ==
                        checkoff_evaluation.checkoff_time) < 0:
                    last_checkoff_evaluation = checkoff_evaluation
        return last_checkoff_evaluation
