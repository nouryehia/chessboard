# needed for annotating return types of the same object
from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from ...setup import db
# from .models import EnrolledCourse
from ..utils.pass_gen import gen_password
from ..security.password import pwd_context


class User(db.Model):
    """
    Represents a user in the DB with relevant functions for
    manipulation of user data.\n
    Fields:
    id --> User ID. Unique, primary key\n
    email --> UCSD (or otherwise) email. Unique field.\n
    first_name --> First name of the user.\n
    last_name --> Surname of the user.\n
    password --> Hashed password of the user.\n
    pid --> PID of the user object. Unique.\n
    last_login --> Date of the last login of the current user.\n
    @author: npcompletenate
    """
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=True)
    pid = db.Column(db.String(10), nullable=True, unique=True)
    last_login = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        """
        Concatenates first and last name.\n
        Params: None\n
        Returns: A string of the user's first and last names
        """
        return self.firstName + " " + self.lastName

    def save(self) -> None:
        '''
        Saves the current object in the DB.\n
        Params: None\n
        Returns: None
        '''
        db.session.commit()

    def update_login_timestamp(self) -> None:
        '''
        Updates the `lastLogin` field of the current user in the
        database.\n
        Params: None\n
        Returns: None
        '''
        # grab current time and update field
        last_login = datetime.now()
        self.last_login = last_login

        # push change to the DB
        self.save()

    def reset_password(self, passwd: str) -> None:
        '''
        Reset the user's password. Is hashed\n
        Params: pass - new password.\n
        Returns: None
        '''
        self.password = pwd_context.hash(passwd)
        self.save()

    def to_json(self) -> Dict[str, str]:
        '''
        Function that takes a user object and returns it in dictionary
        form. Used on the API layer.\n
        Params: none\n
        Returns: Dictionary of the user info
        '''
        ret = {}
        ret['fname'] = self.first_name
        ret['lname'] = self.last_name
        ret['email'] = self.email
        ret['id'] = self.id
        ret['pid'] = self.pid
        ret['last_login'] = self.last_login
        return ret

    @staticmethod
    def check_password(email: str, passwd: str) -> bool:
        '''
        Function that checks if the given password is valid
        for the user with the given email. If the email does not
        map to a valid user, we return `False`.\n
        Params: email - string. User to use.\n
        passwd - string. Given password. At this point, it is still unhashed.\n
        Returns: boolean value.
        '''
        user = User.query.filter_by(email=email).first()
        if user:
            return pwd_context.verify(user.password, passwd)
        return False

    @staticmethod
    def create_user(email: str, f_name: str, l_name: str,
                    pid: str, passwd: str) -> bool:
        '''
        Function that creates a new user object and adds it to the database.\n
        If the password field isn't provided, we randomly generate one for the
        user.\n
        Params: email - string. Email address for the user.\n
        f_name - string. User's first name.\n
        l_name - string. User's surname.\n
        pid - string. PID of the user. Can be null.\n
        passwd - string. User's password. If null, it gets created.\n
        Returns: boolean value
        '''

        # don't try to add someone who already is a user
        if User.find_by_pid_email_fallback(pid, email):
            return False

        if not passwd:
            passwd = gen_password()
        u = User(email=email, first_name=f_name, last_name=l_name, pid=pid,
                 password=pwd_context.hash(passwd))

        db.session.add(u)
        u.save()
        return True

    """
    def get_courses_for_user(self) -> List[EnrolledCourse]:
        '''
        Database query for getting all EnrolledCourses for our user.\n
        Params: None\n
        Returns: A list of EnrolledCourses (can be empty)
        '''
        # TODO: Come back to this and change it to a function call
        # we don't wanna query a different table directly
        return EnrolledCourse.query.filter_by(user_id=self.id).all()
        """

    @staticmethod
    def create_random_password(user) -> None:
        '''
        Function used to generate a random password for a user.\n
        Params: user - User\n
        Returns: None
        '''
        user.password = gen_password()
        user.save()

    @staticmethod
    def find_by_pid_email_fallback(pid: str, email: str) -> Optional[User]:
        '''
        Function that tries to find a user using their PID first,
        then uses their email as a fallback.

        Note that this function may return `None` if the given PID
        and email both do not map to any known users.\n
        Params: pid - string. email - string.\n
        Returns: Optional[User]
        '''
        user = User.query.filter_by(pid=pid).first()

        if not pid or pid == '' or not user:
            user = User.query.filter_by(email=email).first()
        return user

    @staticmethod
    def get_all_users() -> List[User]:
        '''
        Function that returns a list of all users in the database.\n
        Probably shouldn't be used much, given that the user list may be quite
        large.\n
        Params: None\n
        Returns: List[User]
        '''
        return User.query.all()
