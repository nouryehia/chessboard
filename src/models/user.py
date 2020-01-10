from typing import List
from datetime import datetime
from passlib.hash import pbkdf2_sha256

from app import db
from .utils import gen_password
from .models import EnrolledCourse


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
        self.password = pbkdf2_sha256.hash(passwd)
        self.save()

    @staticmethod
    def check_password(email: str, passwd: str) -> bool:
        user = User.query.filter_by(email=email).first()
        if user:
            return pbkdf2_sha256.verify(user.password, passwd)
        return False

    def get_courses_for_user(self) -> List[EnrolledCourse]:
        '''
        Database query for getting all EnrolledCourses for our user.\n
        Params: None\n
        Returns: A list of EnrolledCourses (can be empty)
        '''
        return EnrolledCourse.query.filter_by(user_id=self.id).all()

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
    def find_by_pid_with_email_fallback(pid: str, email: str):
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
