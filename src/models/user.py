# from typing import Optional, List
from datetime import datetime
from app import db


class User(db.Model):
    """
    Represents a user in the DB with relevant functions for
    manipulation of user data.\n
    Fields:
    id --> User ID. Unique, primary key\n
    email --> UCSD (or otherwise) email. Unique field.\n
    firstName --> First name of the user.\n
    lastName --> Surname of the user.\n
    password --> Hashed password of the user.\n
    pid --> PID of the user object. Unique.\n
    lastLogin --> Date of the last login of the current user.\n
    nightMode --> Boolean. Whether user is using night mode or not.
    Deprecated.\n
    @author: npcompletenate
    """
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=True)
    pid = db.Column(db.String(10), nullable=True, unique=True)
    lastLogin = db.Column(db.DateTime, nullable=True)
    nightMode = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        """
        Concatenates first and last name.\n
        Params: None\n
        Returns: A string of the user's first and last names
        """
        return self.firstName + " " + self.lastName

    def update_login_timestamp(self) -> None:
        '''
        Updates the `lastLogin` field of the current user in the
        database.\n
        Params: None\n
        Returns: None
        '''
        # grab current time and update field
        last_login = datetime.now()
        self.lastLogin = last_login

        # push change to the DB
        db.session.commit()
