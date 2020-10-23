from os import getenv
import smtplib as smtp

from .logger import Logger, LogLevels


class MailUtil(object):
    '''
    Utility class for sending emails.
    This class is a true singleton, so you can
    import the class and instantiate it whilst
    only getting the same instance of the object.
    '''
    _instance = None
    _email = None
    _passwd = None
    _host = None
    _port = None

    @classmethod
    def __new__(cls):
        '''
        Implementing singleton pattern in a stricter way than the old method
        Author: @npcompletenate
        '''
        if cls._instance is None:
            Logger.custom_msg('Creating the emailer object')
            cls._instance = super(MailUtil, cls).__new__(cls)
            cls._email = getenv('AG_EMAIL')
            cls._passwd = getenv('AG_PASSWORD')
            cls._host = 'smtp.gmail.com'
            cls._port = 587
        return cls._instance

    def send(self, to: [str], subject: str, body: str) -> bool:
        '''
        Util function for sending an email to any number of users
        @author shaeli and rahul
        Params:
            to      - email address to send to
            subject - subject of the email
            body    - message
        Return: True on successful send, false otherwise
        '''

        try:
            with smtp.SMTP(MailUtil._host, MailUtil._port) as srvr:
                srvr.ehlo()
                srvr.starttls()
                srvr.login(MailUtil._email, MailUtil._passwd)
                msglg = 'Login attempt for donotreply account successful'
                Logger.custom_msg(msglg)

                message = f'Subject: {subject}\n\n{body}'
                srvr.sendmail(MailUtil._email, to, message)
                msglg = f'Successfully sent email to {to}'
                Logger.custom_msg(msglg, LogLevels.INFO)

            return True

        except smtp.SMTPAuthenticationError:
            msglg = 'Login attempt for donotreply account unsuccessful'
            Logger.custom_msg(msglg, LogLevels.ERR)
            return False
