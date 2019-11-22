from app import db

+----------------+------------+------+-----+---------+----------------+
| Field          | Type       | Null | Key | Default | Extra          |
+----------------+------------+------+-----+---------+----------------+
| id             | bigint(20) | NO   | PRI | NULL    | auto_increment |
| checkoffTime   | datetime   | NO   |     | NULL    |                |
| invalidedTime  | datetime   | YES  |     | NULL    |                |
| checkoff_id    | bigint(20) | NO   | MUL | NULL    |                |
| grader_id      | bigint(20) | NO   | MUL | NULL    |                |
| invalidator_id | bigint(20) | YES  | MUL | NULL    |                |
| student_id     | bigint(20) | NO   | MUL | NULL    |                |
+----------------+------------+------+-----+---------+----------------+

'''
    - different cases between db and the model, we should change the db names
    - what is invalidator???
    - new in python
'''
class CheckoffEvaluation(db.Model):
    """
    Represents individual checkoff status for each indiviudal.\n
    Allows graders to checkoff students and evaluate their performance\n
    Fields:
    id --> User ID. Unique, primary key\n
    checkoffTime --> Time of checkoff evaluation by grader
    invalidedTime --> 
    checkoff_id --> Foreign Key to corresponding Checkoff\n
    grader_id --> Foreign Key to grader's user\n
    invalidator_id --> 
    student_id --> Foreign Key to student's user\n
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    checkoff_time = db.Column(db.DateTime, nullable=False)
    invalided_time = db.Column(db.DateTime, nullable=True)
    checkoff = db.Column(db.Integer, db.ForeignKey(Checkoff.id),
                         nullable=False)
    grader = db.Column(db.Integer, db.ForeignKey(Username.id),
                       nullable=False)
    invalidator = db.Column(db.Integer, db.ForeignKey(Username.id),
                            nullable=True)
    student = db.Column(db.Integer, db.ForeignKey(Username.id),
                        nullable=False)

    # don't know what these do
    def is_invalidated(self) -> bool:
        return self.invalidator is not None

    def invalidate(self, invalidator: Username) -> None:
        if not self.is_invalidated():
            self.invalided_time = datetime.now()
            self.invalidator = invalidator
            db.session.commit()

    # Static query methods
    @classmethod
    def create_eval(cls, assignment: Checkoff, grader: Username,
                    student: Username) -> CheckoffEvaluation:
        return new CheckoffEvaluation(assignment, grader, student)

    @classmethod
    def find_checkoff(cls, checkoff_id: int,
                      student_id: int) -> CheckoffEvaluation:
        return CheckoffEvaluation.query.filterby(checkoff=checkoff_id,
                                                 student=student_id,
                                                 invalidator=None).first()

    @classmethod
    def find_newest_checkoff(cls, checkoff_id: int,
                             student_id: int) -> CheckoffEvaluation:
        return CheckoffEvaluation.query.filter_by(checkoff=checkoff_id,
                                                  student=student_id,
                                                  invalidator=None).order_by(desc(checkoff_time)).first()
    
    @classmethod
    def find_invalided(cls, checkoff_id: int,
                       student_id: int) -> CheckoffEvaluation:
        return CheckoffEvalution.query.filterby(checkoff=checkoff_id, student=student_id, invalidator=not None).order_by(desc(invalided_time)).first()

    @classmethod
    def find_newest_checkoff_for_invalidation(cls, checkoff_id: int,
                                              student_id: int) -> CheckoffEvaluation:


        return CheckoffEvaluation.query.filterby(checkoff=checkoff_id, student=student_id).order_by(desc(checkoff_time)).first()

    def __eq__(self, other):

    '''
    public int compareTo(CheckoffEvaluation other){
        //compare the usernames, first by last name
        int lastName = this.checkoffTime.compareTo(other.checkoffTime);
        //if the last names are the same, then we would compare using the first name.
        if(lastName == 0){
            return this.checkoffTime.compareTo(other.checkoffTime);
        }
        return lastName;
    }
    '''

    @staticmethod
    def find_all_for_assignment(self, assignment_id: int) -> CheckoffEvaluation[]:
        return CheckoffEvaluation.query.filterby(checkoff.suite.assignment.id=assignment_id).order_by(desc(checkoff_time)).fetch()

    @staticmethod
    def find_all_for_assignment_for_section(self, assignment_id: int, 
                                            section_id: int) -> CheckoffEvaluation[]:
        Section section = Section.findById(section_id)

        CheckoffEvaluations evaluations[]

        for student in section.usernames:
            evalutions.add(find_all_for_assignment_for_student(assignment_id, student.id))
        
        return evaluations

    @staticmethod
    def find_all_for_assignment_for_section(self, assignment_id: int,
                                            section_id: int) -> CheckoffEvalution[]:
        return CheckoffEvaluation.query.filterby(checkoff.suite.assignment.id = assignment_id, grader=grader_id).fetch()

    @staticmethod
    def find_all_for_assignment_for_grader(self, assignment_id: int,
                                           section_id: int, long grader_id):
        Section section = Section.findById(sectionId)

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