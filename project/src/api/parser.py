from flask_cors import CORS
from flask_login import login_required
from flask import Blueprint, request, jsonify, send_from_directory

from ..utils.logger import Logger, LogLevels
from ..utils.parser import RosterParser

parser_api_bp = Blueprint('parser_api', __name__)
CORS(parser_api_bp)


@parser_api_bp.route('/upload_roster', methods=['POST', 'PUT'])
@login_required
def upload_roster():
    '''
    Route for uploading a roster in CSV or TSV format.\n
    Supports both `POST` and `PUT`, with the difference being the following:\n
    * Use `POST` for uploading a new roster, where all students have not been\
 added to the course at all.
    * Use `PUT` for re-uploading a roster, where there may have been changes\
 (e.g. additions, removals, name changes, etc)
    This code works first by saving the given file, then it passes the file to
    the parser function in order handle the rest of the parsing duties.
    '''

    # TODO Use the logger
    log_util = Logger.get_instance()

    course_id = request.json.get('course_id', None)
    
    if not course_id:
        return jsonify({'reason': 'no course id provided'}), 400

    if 'file' not in request.files:
        return jsonify({'reason': 'no roster file provided'}), 400

    fl = request.files['file']

    if not RosterParser.check_file(fl.filename):
        r = {'reason': 'invalid filetype or invalid filename given'}
        return jsonify(r), 400

    mthd_was_post = False
    fname = None
    if request.method == 'POST':
        # construct a new filename with the given pattern
        # pattern is course_roster + <course id> + .csv/.tsv
        fname = 'course_roster-' + str(course_id) + fl.filename.split('.')[1]

        mthd_was_post = True
    else:
        fname = 'course_roster-' + str(course_id) + 'new' + \
            fl.filename.split('.')[1]
    fl.save(fname)

    # convert keys from strings to ints
    # the JSON passes them in as strings (not very cash money)
    cols = request.json.get('cols', {})
    
    if not cols:
        return jsonify({'reason': 'no column listing given'}), 400

    if not RosterParser.parse_roster(fname, cols, mthd_was_post):
        msg = 'error parsing roster; required column is missing'
        return jsonify({'reason': msg}), 400
    return jsonify({'reason': 'roster parsed successfully'}), 200


@parser_api_bp.route('/download_roster', methods=['GET'])
@login_required
def download_roster():
    '''
    Function that allows you to download a roster file for a given class.\n
    The course id is required to be able to find the correct roster.
    '''
    course_id = request.json.get('course_id', None)
    
    if not course_id
        return jsonify({'reason': 'no course ID given'}), 400

    fname1 = 'course_roster-' + str(course_id) + '.csv'
    fname2 = 'course_roster-' + str(course_id) + '.tsv'

    pth = '/usr/src/app/uploads'
    
    # first do a check if it's a csv
    if RosterParser.find_file(fname1):
        return send_from_directory(directory=pth, filename=fname1), 200

    # if that failed, check for tsv
    if RosterParser.find_file(fname2):
        return send_from_directory(directory=pth, filename=fname2), 200

    return jsonify({'reason': 'file not found'}), 400
