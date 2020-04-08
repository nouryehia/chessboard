
import logging
from datetime import datetime


# Defines the Logger class 
class Logger ():
    def __init__(self, file_count):
        fileName = 'f'+(str)(file_count)+'.log'
        logging.basicConfig(filename=fileName, level=logging.DEBUG)

    def login(self, email):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " " + (str)(email) + " logged in.\n"  
        logging.info(message)

    def invalidCredentials(self, email):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " " +(str)(email) + " attempted with INVALID CREDENTIALS.\n"
        logging.warning(message)

    def logout(self, email):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " " +(str)(email) + " logged out.\n"
        logging.info(message)

    def reset_password(self, email):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " " +(str)(email) + " reset password.\n"
        logging.warning(message)

    def forgot_password(self, email):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " " +(str)(email) + " forgot password and received random password.\n"
        logging.info(message)

    def forgot_password_invalid_email(self, email):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " " +(str)(email) + " forgot password but the email in invalid.\n"
        logging.warning(message)
    
    def addedStudentsToCourseSection(self, firstNames, lastNames, section, course):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " Added the following to " + (str)(section) + " section of the " + (str)(course) + " course : \n"
        for firstName, lastName in zip(firstNames, lastNames):
            message += "-- " + (str)(firstName) + " " + (str)(lastName) + "\n"
        logging.info(message)

    def create_user(self, email: str, f_name: str, l_name: str,
                    pid: str, passwd: str):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " Created new user with \n email : " + email + " \n first name : " + f_name + " \n last name : " + l_name + " \n pid : " + pid + "\n"
        logging.info(message)

    def create_user_fallback(self, email: str):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " Attempted to created new user with email : " + email + " but there exists an associeted account to this email. \n"  
        logging.warning(message)

    def create_course(self, id: int, name: str, short_name: str, quarter: int, year: int ):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " Created coures with ID : " + (str)(id) + ", name : " + name + " - " + short_name + ", for Quarter : " + (str)(quarter) + ", year : " + (str)(year) + "\n" 
        logging.info(message)

    def added_section(self, section_name: str, course_id: int):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " Added section :" + section_name + ", to course with id : " + (str)(course_id) + "\n" 
        logging.info(message)

    def changed_role(self, user_id: int, course_id: int, prev_role: int, new_role: int):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " Changed role of user with ID : " + (str)(user_id) + " for the Course with ID : " + (str)(course_id) + " from " + (str)(prev_role) + " to " + (str)(new_role) + ".\n" 
        logging.info(message)

    def created_ticket(self, user_id: int, course_id: int):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = current_time + " User with ID : " + (str)(user_id) + " created a ticket for the course with ID : " + (str)(course_id) + ".\n" 
        logging.info(message)

'''
# USAGE EXAMPLES
myLogger = Logger(1) 
myLogger.login("mihai")
myLogger.invalidCredentials("mihai")
myLogger.create_course(1, "CSE 12 : Data Structures", "CSE12", 1, 2020)
myLogger.added_section("A01", 1)
myLogger.changed_role(1, 2, 3, 4)
'''