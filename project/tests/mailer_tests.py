import unittest
from src.utils.mailer import MailUtil


class TestStringMethods(unittest.TestCase):

    # Returns True if the string contains 4 a.
    def send_to_one(self):
        mail = MailUtil()
        msg = 'Love looks not with the eyes but with the mind'
        mail.send('edyau@ucsd.edu', 'hello my darling', msg)

    def send_to_many(self):
        emailList = ['edyau@ucsd.edu', 's3yao@ucsd.edu', 'sbalasa@ucsd.edu',
                     'rnemmani@ucsd.edu']
        mail = MailUtil()
        msg = 'To be, or not to be: that is the question'
        mail.send(emailList, 'hello my darlings', msg)

    def send_to_invalid_email(self):
        mail = MailUtil()
        msg = 'Love looks not with the eyes but with the mind'
        mail.send('aiuwefklnsdc@ucsd.edu', 'hello my darling', msg)


if __name__ == '__main__':
    unittest.main()
