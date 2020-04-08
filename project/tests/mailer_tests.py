import unittest
from .src.utils.mailer import MailUtil


class TestStringMethods(unittest.TestCase):

    # Returns True if the string contains 4 a.
    def test_1(self):
        mail = MailUtil()
        mail.send('edyau@ucsd.edu', 'hello my darling', 'Love looks not with the eyes but with the mind')

    def test_2(self):
        emailList = ['edyau@ucsd.edu', 's3yao@ucsd.edu', 'sbalasa@ucsd.edu', 'rnemmani@ucsd.edu']
        mail = MailUtil()
        mail.send(emailList, 'hello my darlings', 'To be, or not to be: that is the question')

    def test_3(self):
        mail = MailUtil()
        mail.send('aiuwefklnsdc@ucsd.edu', 'hello my darling', 'Love looks not with the eyes but with the mind')


if __name__ == '__main__':
    unittest.main()
