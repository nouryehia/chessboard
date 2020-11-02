import unittest
from src.utils.mailer import mailer


class TestStringMethods(unittest.TestCase):

    # Returns True if the string contains 4 a.
    def send_to_one(self):
        msg = 'Love looks not with the eyes but with the mind'
        mailer.send('edyau@ucsd.edu', 'hello my darling', msg)

    def send_to_many(self):
        emailList = ['edyau@ucsd.edu', 's3yao@ucsd.edu', 'sbalasa@ucsd.edu',
                     'rnemmani@ucsd.edu']
        msg = 'To be, or not to be: that is the question'
        mailer.send(emailList, 'hello my darlings', msg)

    def send_to_invalid_email(self):
        msg = 'Love looks not with the eyes but with the mind'
        mailer.send('aiuwefklnsdc@ucsd.edu', 'hello my darling', msg)


if __name__ == '__main__':
    unittest.main()

