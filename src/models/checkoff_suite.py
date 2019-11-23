from app import db


class CheckoffSuite(db.Model):
    """
    Represents the readiness state of Checkoff in the Assignment lifecycle.\n
    Independent of the state of individual submissions\n
    Fields:
    id --> CheckoffSuite ID. Unique, primary key\n
    status --> Checkoff availability status \n
    @author sravyabalasa
    """
    class Status(Enum):
        HIDDEN = 0          # Created but not available to students/graders
        AVAILABLE = 1       # Available to students for submission
        FINALIZED = 2       # Grades submitted, moved to archived state

    __tablename__ = 'CheckoffSuite'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer(11), nullable=False)

    def __init__(self,
                 assignment: Assignment,
                 checkoffs: Checkoff[], **kwargs):
        super(CheckoffSuite, self).__init__(**kwargs)
        self.assignment = assignment
        self.checkoffs = checkoffs

    def is_hidden(self) -> bool:
        return status == Status.HIDDEN

    def is_available(self) -> bool:
        return status == Status.AVAILABLE

    def is_finalized(self) -> bool:
        return status == Status.FINALIZED

    def set_hidden(self) -> None:
        status = Status.HIDDEN
        db.session.commit()

    def set_available(self) -> None:
        status = Status.AVAILABLE
        db.session.commit()

    def set_finalized(self) -> None:
        status = Status.FINALIZED
        db.session.commit()

    def add_checkoff(self, Checkoff checkoff) -> None:
        checkoffs.add(checkoff)
        db.session.commit()

    def get_max_score(self) -> int:
        for checkoff in checkoffs:
            total += checkoff.points
        return total

    def get_score_for_student(self, long studentId) -> int:
        for checkoff in checkoffs:
            if (CheckoffEvaluation.findCheckoff(checkoff.id, studentId)
                    is not None):
                total += 1
        return total

    def get_newest_checkoff_evaluation_for_student(self,
                                                   long studentId) -> long:
        for checkoff in checkoffs:
            checkoff_evaluation = CheckoffEvaluation.findNewestCheckoff(checkoff.id, studentId)
            if checkoff_evaluation is not None:
                if last_checkoff_evaluation is None:
                    last_checkoff_evaluation = checkoff_evaluation
                else if (last_checkoff_evaluation.checkoff_time ==
                        checkoff_evaluation.checkoff_time) < 0:
                    last_checkoff_evaluation = checkoff_evaluation
        return last_checkoff_evaluation
