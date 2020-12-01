import os
import csv
from typing import Dict, Tuple

from ..models.user import User
from .mailer import MailUtil
from .logger import Logger, LogLevels


class RosterParser(object):
    '''
    Utility class for parsing course rosters.\n
    Can create new students, remove/rename students in roster, and more.\n
    @author npcompletenate
    '''

    @staticmethod
    def check_file(filename: str) -> bool:
        '''
        Helper to check if the filename given is valid.\n
        Valid filenames end with '.tsv' or '.csv'
        '''
        if filename == '' or filename.count('.') != 1:
            return False
        val = filename.split('.')[1]
        return val == 'tsv' or val == 'csv'

    @staticmethod
    def parse_roster(filename: str, cols: Dict[str, int], mthd: bool) -> bool:
        '''
        This function parses a given file. Can be used to change rosters or to
        create a new roster for a course.\n
        `cols` is a mapping of the column description to the index number in
        the file.\n
        `mthd` is `True` when doing a new import and `False` otherwise.\n
        The function returns a boolean signifying successful import.
        '''
        def process_name(name: str) -> Tuple[str, str]:
            '''
            This separates a name passed in as Last,First
            '''
            return name.split(',')[1], name.split(',')[0]

        log_util = Logger.get_instance()

        filename = '/usr/src/app/uploads/' + filename

        is_csv = ',' if filename.split('.')[1] == 'csv' else '\t'

        # get indices for the corresponding columns in the CSV/TSV
        try:
            name_idx = cols['name']
            pid_idx = cols['pid']
            email_idx = cols['email']
            course_idx = cols['course_id']
            section_idx = cols['section_id']
        except KeyError:
            msg = 'Missing expected column from file.'
            log_util.custom_msg(LogLevels.ERR, msg)
            return False

        with open(filename, 'r', newline='') as infile:
            reader = csv.reader(infile, delimiter=is_csv)

            # this means that we're adding all new students
            if mthd:
                names = []
                for row in reader:

                    # assign variables from fields in the row
                    email = row[email_idx]
                    pid = row[pid_idx]
                    fname, lname = process_name(row[name_idx])
                    names.append(row[name_idx])
                    course_id = row[course_idx]
                    section_id = row[section_idx]

                    usr = User.find_by_pid_email_fallback(pid, email)
                    if not usr:
                        _, pwrd, usr = User.create_user(email, fname, lname,
                                                        pid, None)

                        # this means we generated a password for the new
                        # account
                        if pwrd:
                            sub = 'Created Account and Added To Course'
                            msg = 'Hello!\nYou\'re receiving this email' +\
                                ' because an account was created for' +\
                                ' you on autograder.ucsd.edu.\n' +\
                                'You\'ve been given a temporary password;' +\
                                'please go change it as soon as possible!' +\
                                f' Your password is {pwrd}.\n' +\
                                'Have a great day!\nCheers,\n' +\
                                'The Autograder Team'
                            MailUtil.get_instance().send(email, sub, msg)
                            log_util.create_user(usr)

                    # TODO add usr to course and to section

                log_util.add_students_section(names, str(section_id),
                                              str(course_id))

            else:
                # this means that we may be doing roster updates
                pass
        return True

    @staticmethod
    def find_file(filename: str) -> bool:
        '''
        Function that walks through the directory structure looking
        for a particular file with name `filename`. Returns a boolean
        and the found string name (if applicable) or `None` if no such file
        with that name exists.
        '''
        for _, _, files in os.walk('/usr/src/app/uploads'):
            return filename in files
        return False
