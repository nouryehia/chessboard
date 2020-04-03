from os import getenv
import smtplib as slib


class MailUtil(object):
    '''
    '''

    email = getenv('AG_EMAIL')
    passwd = getenv('AG_PASSWD')
