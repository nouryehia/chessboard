from __future__ import annotations

from ...setup import db
from typing import List, Optional, Dict

# import other models after they are merged
# from .models.category import Category
# from .models.checkoffsuite import CheckoffSuite
# from .models.course import Course


class Assignment(db.Model):
    '''
    Represents an assignment in the DB with relevant functions for\
    manipulation of user data. \n
    Fields: \n
    id --> Assigment ID. Unique, primary key. \n
    due --> Assignment due date. \n
    is_deleted --> Deleted status of assignment. \n
    name --> Name of the assignment. \n
    category_id --> Weighted category of assignment. \n
    checkoff_suite_id --> Readiness state of checkoff. \n
    total_grade_percent --> Percent of total grade of assignment. \n
    @author: tiffany-meng\n
    '''
    __tablename__ = 'Assignment'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    due = db.Column(db.DateTime, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    # db.ForeignKey(Category.id) wait to be merged
    course_id = db.Column(db.Integer, nullable=False)
    # db.ForeignKey(Course.id) wait to be merged
    checkoff_suite_id = db.Column(db.Integer, nullable=False)
    # db.ForeignKey(CheckoffSuite.id) wait to be merged
    total_grade_percent = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        '''
        Returns the name of the assignment as a string.\n
        Params: None\n
        Returns: A string containing the name of the assignment.
        '''
        return self.name

    def save(self) -> None:
        '''
        Saves current object in the DB.\n
        Params: None\n
        Returns: None\n
        '''
        db.session.commit()

    def to_json(self) -> Dict[str, str]:
        ret = {}
        ret['id'] = self.id
        ret['due'] = self.due
        ret['name'] = self.name
        ret['category'] = self.category_id
        ret['course'] = self.course_id
        ret['checkoffsuite'] = self.checkoff_suite_id
        ret['percent'] = self.total_grade_percent
        return ret

    def soft_delete(self) -> Assignment:
        '''
        Sets the assignment to deleted and returns this assignment.\n
        Params: None\n
        Returns: This assignmnet.
        '''
        self.is_deleted = True
        self.save()
        return self

    def restore(self) -> Assignment:
        '''
        Restores this assignment and returns the assignment.\n
        Params: None\n
        Returns: This assignment.
        '''
        self.is_deleted = False
        self.save()
        return self

    def get_status(self):
        '''
        Gets the status of the assignment.\n
        Params: None\n
        Returns: An Enum representing the status of the assignment\n
        **hard to annotate Enum**
        '''

        '''
        c_suite = CheckoffSuite.find_by_id(self.checkoff_suite_id)
        return c_suite.status if c_suite else None
        TODO: wait for CheckoffSuite to be merged
        '''

    # def get_course(self) -> Optional[Course]:
        '''
        Gets the course of the assignment.\n
        Params: None\n
        Returns: The course of the assignment
        '''

        '''
        crs = Coure.find_by_id(self.course_id)
        return crs
        # TODO: wait for Course merge
        '''

    def is_hidden(self) -> bool:
        '''
        Checks if assignment is hidden.\n
        Params: None\n
        Returns: A boolean representing if the assignmnet is hidden.\n
        '''

        '''
        c_suite = CheckoffSuite.find_by_id(self.checkoff_suite_id)
        return c_suite.is_hidden() if c_suite else False
        TODO: wait for CheckoffSuite merge
        '''

    def set_available(self) -> None:
        '''
        Sets the assignment to available.\n
        Params: None\n
        Returns: None\n
        '''
        '''
        c_suite = CheckoffSuite.find_by_id(self.checkoff_suite_id)
        if c_suite:
            c_suite.set_available()
        self.save()
        TODO: wait for CheckoffSuite merge
        '''

    def set_finalized(self) -> None:
        '''
        Sets the assignment to finalized.\n
        Params: None\n
        Returns: None\n
        '''

        '''
        c_suite = CheckoffSuite.find_by_id(self.checkoff_suite_id)
        if c_suite:
            c_suite.set_finalized()
        self.save()
        TODO: wait for CheckoffSuite merge
        '''

    @staticmethod
    def create_assignment(due: int, name: str, category: int, course: int,
                          checkoff_suite: int, percent: float) -> None:
        '''
        Create a new assignment object and add it to the database.\n
        Params: due - due date of the assignment\n
        name - name of the assignment\n
        category - id of category that assignment is in\n
        course - id of course that assignment is in\n
        checkoff_suite - id of checkoff suite that assignment is in\n
        percent - percent of total grade\n
        '''
        a = Assignment(due=due, is_deleted=False, name=name,
                       category_id=category, course_id=course,
                       checkoff_suite_id=checkoff_suite,
                       total_grade_percent=percent)
        db.session.add(a)
        a.save()

    @staticmethod
    def find_assignment(assignment_id: int) -> Assignment:
        '''
        Returns the assignment for the assignment id passed in.\n
        Params: id of assignment to find\n
        Returns: An assignment matching the id\n
        '''
        return Assignment.query.filter_by(id=assignment_id,
                                          is_deleted=False).first()

    @staticmethod
    def find_all_for_category(category_id: int) -> List[Assignment]:
        '''
        Returns a list of assignments for a given category id passed in.\n
        Params: category id of the assignments\n
        Returns: A list of available assignments for a category\n
        '''
        return Assignment.query.filter_by(category_id=category_id).all()

    @staticmethod
    def find_all_for_course(course_id: int) -> Optional[Assignment]:
        '''
        Returns a list of assignments for a given course id passed in.\n
        Params: course id of the assignments\n
        Returns: A list of assignments for a course.\n
        '''
        ret = Assignment.query.filter_by(course_id=course_id,
                                         is_deleted=False).all()
        return ret if ret else None

    @staticmethod
    def delete_asn_for_course(cs_id: int, asn_id: int) -> Optional[Assignment]:
        '''
        Deletes an assignment in a specific course.\n
        Params: the course id of the assignment, the id of the assignment.\n
        Returns: None\n
        '''
        asn = Assignment.query.filter_by(course_id=cs_id, id=asn_id,
                                         is_deleted=False).first()
        if not asn:
            return None
        else:
            asn.soft_delete()
            return asn

    @staticmethod
    def delete_all_for_course(course_id: int) -> None:
        '''
        Deletes all assignments for a course.\n
        Params: the course to delete the assignments for\n
        Returns: None\n
        '''
        assignment_list = Assignment.query.filter_by(course_id=course_id).all()
        for assignment in assignment_list:
            assignment.soft_delete()
        db.session.commit()

    @staticmethod
    def restore_asn_for_course(cs_id: int, as_id: int) -> Optional[Assignment]:
        asn = Assignment.query.filter_by(course_id=cs_id, id=as_id,
                                         is_deleted=True).first()
        if not asn:
            return None
        else:
            asn.restore()
            return asn

    @staticmethod
    def restore_all_for_course(course_id: int) -> None:
        '''
        Restores all deleted assignments for a course.\n
        Params: the course to restore the assignments for\n
        Returns: None\n
        '''
        assignment_list = Assignment.query.filter_by(course_id=course_id).all()
        for assignment in assignment_list:
            assignment.restore()
        db.session.commit()
