from app import db


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
    checkoff = db.Column(db.Integer, db.ForeignKey(Checkoff.id),
                         nullable=False)
    grader = db.Column(db.Integer, db.ForeignKey(User.id),
                       nullable=False)
    student = db.Column(db.Integer, db.ForeignKey(User.id),
                        nullable=False)

    # Static query methods
    @classmethod
    def create_eval(cls, assignment: Checkoff, grader: User,
                    student: User) -> CheckoffEvaluation:
        return CheckoffEvaluation(assignment, grader, student)

    @classmethod
    def find_checkoff(cls, checkoff_id: int,
                      student_id: int) -> CheckoffEvaluation:
        return CheckoffEvaluation.query.filterby(checkoff=checkoff_id,
                                                 student=student_id).first()

    @classmethod
    def find_newest_checkoff(cls, checkoff_id: int,
                             student_id: int) -> CheckoffEvaluation:
        return CheckoffEvaluation.query.filter_by(checkoff=checkoff_id,
                                                  student=student_id).order_by(desc(checkoff_time)).first()

    @staticmethod
    def find_all_for_assignment(self, assignment_id: int) -> CheckoffEvaluation[]:
        return CheckoffEvaluation.query.filterby(checkoff.suite.assignment.id=assignment_id).order_by(desc(checkoff_time)).fetch()

    @staticmethod
    def find_all_for_assignment_for_section(self, assignment_id: int, 
                                            section_id: int) -> CheckoffEvaluation[]:
        section = Section.findById(section_id)
        CheckoffEvaluations evaluations[]
        for student in section.usernames:
            evalutions.add(find_all_for_assignment_for_student(assignment_id, student.id))
        return evaluations

    @staticmethod
    def find_all_for_assignment_for_section(self, assignment_id: int,
                                            section_id: int) -> CheckoffEvalution[]:
        return CheckoffEvaluation.query.filterby(checkoff.suite.assignment.id=assignment_id, grader=grader_id).fetch()

    @staticmethod
    def find_all_for_assignment_for_grader(self, assignment_id: int,
                                           section_id: int, long grader_id):
        section = Section.findById(sectionId)
        CheckoffEvaluations evaluations[]
        for student in section.usernames:
            evaluations.add(find_all_for_assignment_for_student_for_grader(assignment_id. student.id))
        return evaluations

    @staticmethod
    def find_all_for_assignment_for_student(self, assignment_id: int,
                                            student_id: int) -> CheckoffEvaluation[]:
        return CheckoffEvaluation.query.filterby(checkoff.suite.assignment.id=assignment_id, student=student_id).fetch()

    @staticmethod
    def find_all_for_assignment_for_student_for_grader(self, assignment_id: int, 
                                                       student_id: int) -> CheckoffEvaluation[]:
        return CheckoffEvaluation.query.filterby(checkoff.suite.assignment.id=assignment_id, student=student_id, grader=grader_id).fetch()