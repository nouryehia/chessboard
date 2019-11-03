from app import db


class CheckoffSuite(db.Model):
    """
    Represents the state of Checkoff in the Assignment lifecycle.\n
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

    def __init__(self, **kwargs):
        super(CheckoffSuite, self).__init__(**kwargs)

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
            checkoffEvaluation = CheckoffEvaluation.findNewestCheckoff(checkoff.id, studentId)
            if checkoffEvaluation is not None:
                if lastCheckoffEvalution is None:
                    lastCheckoffEvaluation = checkoffEvaluation
                else if lastCheckoffEvalution.checkoffTime ==
                        checkoffEvaluation.checkoffTime) < 0:
                    lastCheckoffEvaluation = checkoffEvaluation
        return lastCheckoffEvaluation
