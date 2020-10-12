import ssl
from os import getenv
import smtplib as smtp

from .logger import log_util, LogLevels


class MailUtil(object):
    '''
    Utility class for sending emails.
    '''

    def __init__(self):
        self.email = getenv('AG_EMAIL')
        self.passwd = getenv('AG_PASSWORD')
        self.host = 'smtp.gmail.com'
        self.port = 587

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
            # context = ssl.create_default_context()
            with smtp.SMTP(self.host, self.port) as srvr:
                srvr.ehlo()
                srvr.starttls()
                srvr.login(self.email, self.passwd)
                msglg = 'Login attempt for donotreply account successful'
                log_util.custom_msg(msglg)

                message = f'Subject: {subject}\n\n{body}'
                srvr.sendmail(self.email, to, message)
                msglg = f'Successfully sent email to {to}'
                log_util.custom_msg(msglg, LogLevels.INFO)

            return True

        except smtp.SMTPAuthenticationError:
            msglg = 'Login attempt for donotreply account unsuccessful'
            log_util.custom_msg(msglg, LogLevels.ERR)
            return False


# IMPORT THIS OBJECT
# This is a singleton!
mailer = MailUtil()
