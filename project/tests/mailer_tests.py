# DEPRECATED: Uses unittest
import unittest
from project.src.utils.mailer import MailUtil as Mailer


class TestMailMethods(unittest.TestCase):

    # Returns True if the string contains 4 a. <- What 'string' + How do you check this?
    def send_to_one(self):
        msg = 'Love looks not with the eyes but with the mind'
        success = Mailer.send('edyau@ucsd.edu', 'hello my darling', msg)
        self.assertTrue(success)

    def send_to_many(self):
        email_list = ['edyau@ucsd.edu', 's3yao@ucsd.edu', 'sbalasa@ucsd.edu',
                     'rnemmani@ucsd.edu']
        msg = 'To be, or not to be: that is the question'
        success = Mailer.send(email_list, 'hello my darlings', msg)
        self.assertTrue(success)

    def send_to_invalid_email(self):
        msg = 'Love looks not with the eyes but with the mind'
        success = Mailer.send('aiuwefklnsdc@ucsd.edu', 'hello my darling', msg)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
