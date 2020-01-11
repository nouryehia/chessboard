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

    """
    Creates a new checkoff evaluation\n
    Fields:
    assignment --> Checkoff assignment\n
    grader --> Grader for the checkoff\n
    student --> User who the checkoff belongs to\n
    """
    @staticmethod
    def create_eval(assignment: Checkoff, grader: User,
                    student: User):
        return CheckoffEvaluation(assignment, grader, student)

    """
    Finds checkoff evaluated for the student\n
    Fields:
    checkoff_id --> ID of the checkoff assignment\n
    student_id --> ID of the student\n
    """
    @staticmethod
    def find_checkoff(checkoff_id: int,
                      student_id: int):
        return CheckoffEvaluation.query \
            .filter_by(checkoff_id=checkoff_id,
                       student_id=student_id).first()

    """
    Find the newest checkoff evaluated for the student\n
    Fields:
    checkoff_id --> ID of the checkoff\n
    student_id --> ID of the student\n
    """
    @staticmethod
    def find_newest_checkoff(checkoff_id: int,
                             student_id: int):
        return CheckoffEvaluation.query \
            .filter_by(checkoff_id=checkoff_id, student_id=student_id) \
            .order_by(self.checkoff_time).desc().first()

    """
    Finds all checkoffs evaluated for the student by current grader
    for assignment\n
    Fields:
    assignment_id --> ID of the assignment that is checked off\n
    student_id --> ID of the student\n
    """
    @staticmethod
    def find_all_for_assignment_for_student_for_grader(assignment_id: int,
                                                       student_id: int,
                                                       grader_id: int):
        return CheckoffEvaluation.query \
            checkoff.suite_id.assignment_id=assignment_id
                .filter_by(checkoff.suite_id.assignment_id=assignment_id,
                           student_id=student_id, grader_id=grader_id).fetch()

    """
    Finds all checkoffs evaluated by the grader for that assignment\n
    Fields:
    assignment_id --> ID of the assignment that is checked off\n
    section_id --> ID of the section\n
    grader_id --> ID of the grader\n
    """
    @staticmethod
    def find_all_for_assignment_for_grader(assignment_id: int,
                                           section_id: int,
                                           grader_id: int):
        section = Section.findById(section_id)
        evaluations = []
        for student in section.usernames:
            evaluations.add(find_all_for_assignment_for_student_for_grader
                            (assignment_id, student_id))
        return evaluations

    @staticmethod
    def find_all_for_assignment(self, assignment_id: int):
        """
        Finds all checkoffs evaluated for that assignment\n
        Fields:
        assignment_id --> ID of the assignment that is checked off\n
        """
        return CheckoffEvaluation.query \
            .filter_by(checkoff.suite_id.assignment_id=assignment_id) \
            .order_by(checkoff_time).desc.fetch()

    @staticmethod
    def find_all_for_assignment_for_student(assignment_id: int,
                                            student_id: int):
        """
        Finds checkoffs evaluated for the student for that assignment\n
        Fields:
        assignment_id --> ID of the assignment that is checked off\n
        student_id --> ID of the student\n
        """
        return CheckoffEvaluation.query \
            .filter_by(assignment_id=checkoff.suite.assignment_id,
                       student=student_id).fetch()

    @staticmethod
    def find_all_for_assignment_for_section(assignment_id: int,
                                            section_id: int):
        """
        Finds all checkoffs evaluated for a section for that assignment
        Fields:
        assignment_id --> ID of the assignment that is checked off
        section_id --> ID of the student\n
        """
        section = Section.findById(section_id)
        evaluations = []
        for student in section.usernames:
            evaluations \
                .add(find_all_for_assignment_for_student(assignment_id,
                                                         student_id))
        return evaluations
