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
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    checkoff_time = db.Column(db.DateTime, nullable=False)
    checkoff_id = db.Column(db.Integer, db.ForeignKey(Checkoff.id),
                            nullable=False)
    grader_id = db.Column(db.Integer, db.ForeignKey(User.id),
                          nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(User.id),
                           nullable=False)

    def create_eval(self, assignment: Checkoff, grader: User,
                    student: User):
        return CheckoffEvaluation(assignment, grader, student)

    def find_checkoff(self, checkoff_id: int,
                      student_id: int):
        return CheckoffEvaluation.query.filter_by(checkoff=checkoff_id,
                                                  student=student_id).first()

    def find_newest_checkoff(self, checkoff_id: int,
                             student_id: int):
        return CheckoffEvaluation.query \
            .filter_by(checkoff=checkoff_id, student=student_id) \
            .order_by(self.checkoff_time).desc().first()

    def find_all_for_assignment_for_student_for_grader(self,
                                                       assignment_id: int,
                                                       student_id: int):
        return CheckoffEvaluation.query \
                .filter_by(assignment_id=self.checkoff.suite.assignment_id,
                           student=student_id, grader=self.grader_id).fetch()

    def find_all_for_assignment_for_grader(self, assignment_id: int,
                                           section_id: int,
                                           grader_id: int):
        section = Section.findById(section_id)
        evaluations = []
        for student in section.usernames:
            evaluations.add(self
                            .find_all_for_assignment_for_student_for_grader
                            (assignment_id, self.student_id))
        return evaluations

    def find_all_for_assignment(self, assignment_id: int):
        return CheckoffEvaluation.query \
            .filter_by(assignment_id=self.checkoff.suite_id.assignment_id) \
            .order_by(self.checkoff_time).desc.fetch()

    def find_all_for_assignment_for_student(self, assignment_id: int,
                                            student_id: int):
        return CheckoffEvaluation.query \
                .filter_by(assignment_id=self.checkoff.suite.assignment_id,
                           student=student_id).fetch()

    def find_all_for_assignment_for_section(self, assignment_id: int,
                                            section_id: int):
        section = Section.findById(section_id)
        evaluations = []
        for student in section.usernames:
            evaluations \
                .add(self.find_all_for_assignment_for_student(assignment_id,
                                                              self.student_id))
        return evaluations
