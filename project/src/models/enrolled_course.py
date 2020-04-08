from __future__ import annotations

from ...setup import db
from enum import Enum
from typing import List, Optional
from .models import queue as q
from .models import course as crs  # prentending
from .models import user as usr  # prentending
from .models import sections as sec  # prentending


class Status(Enum):
    """
    Describe the corresponidng status of a user in the class (queue).
    The following fields are defined as name --> database value:\n
    Fields:\n
    ACTIVE --> 0\n
    INACTIVE --> 1\n
    BUSY --> 2\n
    @author: YixuanZhou
    """
    ACTIVE = 0
    INACTIVE = 1
    BUSY = 2


class Role(Enum):
    """
    All the roles that a user can have for a class.\n
    The following fields are difend as name --> database value:\n
    Fields --> Database Value:\n
    ROOT --> 0\n
    ADMIN --> 1\n
    INSTRUCTOR --> 2\n
    GRADER --> 3\n
    STUDENT --> 4\n
    @author: YixuanZhou
    """
    ROOT = 0
    ADMIN = 1
    INSTRUCTOR = 2
    GRADER = 3
    STUDENT = 4


class EnrolledCourse(db.Model):
    """
    The enrolled course database model.\n
    All students should be in the sections that is corresponding to their
    enrollment.\n
    All the instructors / tutors shoud be in a dummy section.\n
    When a student drop from the class, we should clear that row of entry by
    calling delete_enrolled_user.\n
    Fields: \n
    id --> The id of the queue, unique primary key.\n
    user_id --> Forienkey to the user id corresponding to this entry\n
    role --> The role of the user in this class.\n
    section_id --> The forienkey to the section id
                            at high capacity, not nullable.\n
    status --> The status of a user in the class.(mainly for tutor status)\n
    course_id --> The id of the coures that the user is enrolled in.\n
    @author YixuanZhou
    """
    __tablename__ = 'Queue'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=True)
    section_id = db.Column(db.Integer, db.Forienkey('section.id'),
                           nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
                          nullable=False)
    status = db.Column(db.Integer, nullable=False, default=Status.INACTIVE)

    def __init__(self, **kwargs):
        """
        Constructor of the class Enrolled Course.\n
        Inputs:\n
        user_id --> The id of the corresponding user object.\n
        role --> The role of this user in this course.\n
        section_id --> The section the student is in.\n
        course_id --> The id of the coures that the user is enrolled in.\n
        status --> The current status of the user (grader), default
        inactive.\n
        """
        super(EnrolledCourse, self).__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return the string cancatenation of the user_id, role, section_id,
        course_id and status.\n
        Inputs:\n
        None\n
        Returns:\n
        A string representation of the enrolled_course object.\n
        """
        return "user_id: " + self.user_id + " role: " + self.role +\
               " section_id " + self.section_id + " course_id " +\
               self.course_id + " status: " + self.status

    def __eq__(self, other):
        """
        Override the comparison functions of the objects.\n
        Inputs:\n
        The other object of the same type to compare.\n
        Returns:\n
        True if their user_id are the same, meaning they represents the same
        objects.\n
        False otherwise.\n
        """
        if isinstance(other, self.__class__):
            return self.user_id == other.user_id
        else:
            return False

    def __hash__(self):
        """
        The has method for the object, we hash the user_id field.\n
        Returns:\n
        The hash result for the user_id field.\n
        """
        return hash(self.user_id)

    def get_role(self) -> Role:
        """
        Get the role of this EnrolledCourse entry.\n
        Return:\n
        The Role type.
        """
        return self.role

    def get_status(self) -> Role:
        """
        Get the role of this EnrolledCourse entry.\n
        Return:\n
        The Role type.
        """
        return self.status

    def change_role(self, role: Role) -> bool:
        """
        Change the role of the user in this class.\n
        Inputs:\n
        role --> The role to change.\n
        Return:\n
        Whether the change is successed.
        """
        self.role = role
        self.save()
        return True

    def change_status(self, status: Status) -> bool:
        """
        Change the status of the user in this class.\n
        Inputs:\n
        status --> The status to change.\n
        Return:\n
        Whetehr the change is successed.
        """
        self.status = status
        self.save()
        return True

    def save(self):
        """
        Update the object to the database.\n
        """
        db.session.commit()


@staticmethod
def enroll_user(enrolled_user: EnrolledCourse) -> bool:
    """
    Add an enrolled user into the course.\n
    Inputs:\n
    enrolled_user --> The EnrolledCourse object to add.\n
    Return:\n
    Whether the user is added.
    """
    db.session.add(enrolled_user)
    db.session.commit()
    return True


@staticmethod
def enroll_user_to(user_id: int, course_id: int,
                   section_id: int, role: Role) -> bool:
    """
    Enroll a student to a course with corresponding sections.\n
    All the non-student users should be enrolled in to a dummy section.\n
    Inputs:\n
    user_id --> The user_id of the user to enroll.\n
    course_id --> The course_id that the user is enrolled to.\n
    section_id --> The section_id object that the user is enrolled to.\n
    role --> The role of the user in the class.\n
    Return:\n
    Whether the user is added.
    """
    enroll_student = EnrolledCourse(user_id=user_id,
                                    role=role,
                                    section_id=section_id,
                                    status=Status.ACTIVE,
                                    course_id=course_id)
    return enroll_user(enroll_student)


@staticmethod
def find_user_in_course(user_id: int,
                        course_id: int) -> Optional(EnrolledCourse):
    """
    Find a user which is in a specific course.\n
    Inputs:\n
    user_id --> The User id to search for.\n
    course_id --> The Course id to search for.\n
    Return:\n
    A enrolled course entry of the particular user.\n
    """
    return EnrolledCourse.query.filter_by(course_id=course_id,
                                          user_id=user_id).first()


@staticmethod
def find_all_user_in_course(course_id: int,
                            role: Role = None) -> List[EnrolledCourse]:
    """
    Get a list of all the entries corresponding a course.\n
    There can be extra parameter provided which is role.\n
    Inputs:\n
    course --> The Course object to look for.\n
    role --> (Optional) the role to look for.\n
    """
    if not role:
        return EnrolledCourse.query.filter_by(course_id=course_id).all()
    else:
        return EnrolledCourse.query.filter_by(course_id=course_id,
                                              role=role).all()


@staticmethod
def find_user_in_all_course(user_id: int,
                            role: Role = None) -> List[EnrolledCourse]:
    """
    Get a list of all the entries corresponding a user.\n
    There can be extra parameter provided which is role.\n
    Inputs:\n
    user --> The User object to look for.\n
    role --> (Optional) the role to look for.\n
    """
    if not role:
        return EnrolledCourse.query.filter_by(user_id=user_id).all()
    else:
        return EnrolledCourse.query.filter_by(user_id=user_id,
                                              role=role).all()


@staticmethod
def find_active_tutor_for(queue_id: int) -> List[usr.User]:
    """
    Find all the active tutor for a given queue object.\n
    Inputs:\n
    The Queue object to search for.\n
    Returns:\n
    A list of active tutors User objects.\n
    """
    queue = q.find_course_by_id(queue_id)  # TODO
    course = crs.find_course_for(queue)  # need to ask

    grader_enrolled_course = EnrolledCourse.query\
        .filter_by(roles=Role.GRADER)\
        .filter_by(course_id=course.id).all()

    # Since each tutor might be enrolled in multiple sections,
    # we remove the duplicates here.
    grader_set = set()
    grader_set.update(grader_enrolled_course)
    grader_list = []
    for grader in list(grader_set):
        grader_list.append(usr.find_user(id=grader.id))  # need to ask
    return grader_list


@staticmethod
def delete_enrolled_user_from_course(user_id: int, course_id: int):
    """
    Delete an entry from the enrolled_course table.\n
    Inputs:\n
    user_id --> The user_id of the user to delete.\n
    course_id --> The course_id of the course to delete user from.\n
    """
    enrolled_user = find_user_in_course(user_id=user_id, course_id=course_id)
    if enroll_user:
        db.session.delete(enrolled_user)
        db.session.commit()
        return True
    else:
        return False
