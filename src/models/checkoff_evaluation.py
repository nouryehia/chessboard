from app import db
from checkoff import Checkoff
from section import Section
from user import User


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
                    student: User):
        """
        Creates a new checkoff evaluation\n
        Fields:
        assignment --> Checkoff assignment\n
        grader --> Grader for the checkoff\n
        student --> User who the checkoff belongs to\n
        """
        return CheckoffEvaluation(assignment, grader, student)

    @staticmethod
    def find_checkoff(checkoff_id: int,
                      student_id: int):
        """
        Finds checkoff evaluated for the student\n
        Fields:
        checkoff_id --> ID of the checkoff assignment\n
        student_id --> ID of the student\n
        """
        return CheckoffEvaluation.query \
            .filter_by(checkoff_id=checkoff_id,
                       student_id=student_id).first()

    def find_newest_checkoff(self, checkoff_id: int,
                             student_id: int):
        """
        Find the newest checkoff evaluated for the student\n
        Fields:
        checkoff_id --> ID of the checkoff\n
        student_id --> ID of the student\n
        """
        return CheckoffEvaluation.query \
            .filter_by(checkoff_id=checkoff_id, student_id=student_id) \
            .order_by(self.checkoff_time).desc().first()
