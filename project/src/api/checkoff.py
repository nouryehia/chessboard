from flask_cors import CORS
from flask import Blueprint, request, jsonify

from ..models.checkoff import CheckoffEvaluation, Checkoff
from ..models.user import User
from ..models.course import Course

from ..utils.mailer import MailUtil
from ..utils.logger import Logger, LogLevels

checkoff_api_bp = Blueprint('checkoff_api', __name__)
CORS(checkoff_api_bp, supports_credentials=True)


@checkoff_api_bp.route('/create_checkoff', methods=['POST'])
def create_checkoff():
    '''
    Route used to create a new checkoff. Creates a checkoff and returns
    the checkoff object.\n
    @author sravyabalasa
    '''
    description = request.json.get('description', None)
    name = request.json.get('name', None)
    course_id = request.json.get('course_id', None)
    points = request.json.get('points', None)
    status = request.json.get('status', None)
    due = request.json.get('due', None)

    checkoff = Checkoff.create_checkoff(description, name,
                                        course_id, points, due)

    actions = {'hidden': checkoff.set_hidden,
               'available': checkoff.set_available,
               'finalized': checkoff.set_finalized}
    actions[status]()

    return jsonify({'reason': 'checkoff successfully created',
                    'checkoff': checkoff.to_json()}), 200


@checkoff_api_bp.route('/update_checkoff', methods=['PUT'])
def update_checkoff():
    '''
    Route used to update an existing checkoff in the database. Returns
    updated checkoff object.\n
    @author sravyabalasa
    '''
    id = request.json.get('id', None)
    description = request.json.get('description', None)
    name = request.json.get('name', None)
    points = request.json.get('points', None)
    status = request.json.get('status', None)
    due = request.json.get('due', None)

    checkoff = Checkoff.get_checkoff_by_id(id)
    checkoff.update_checkoff(description, name, points, due)

    actions = {'hidden': checkoff.set_hidden,
               'available': checkoff.set_available,
               'finalized': checkoff.set_finalized}
    actions[status]()

    return jsonify({'reason': 'checkoff successfully updated',
                    'checkoff': checkoff.to_json()}), 200


@checkoff_api_bp.route('/delete_checkoff', methods=['PUT'])
def delete_checkoff():
    '''
    Route used to soft delete a checkoff in the database.\n
    Returns deleted checkoff object.\n
    @author sravyabalasa
    '''
    id = request.json.get('id', None)

    checkoff = Checkoff.get_checkoff_by_id(id)
    checkoff.soft_delete()

    return jsonify({'reason': 'checkoff successfully deleted',
                    'checkoff': checkoff.to_json()}), 200


@checkoff_api_bp.route('/get_all_checkoffs_in_course', methods=['GET'])
def get_all_checkoffs():
    '''
    Route used to get all the non-deleted checkoffs in the course from the
    database.\n
    @author sravyabalasa
    '''
    course_id = request.args.get('course_id', None, type=int)

    checkoffs = Checkoff.find_all_checkoffs_in_course(course_id)
    ret = list(map(lambda checkoff: checkoff.to_json(), checkoffs))
    return jsonify({'reason': 'checkoffs found for course',
                    'checkoffs': ret}), 200


@checkoff_api_bp.route('/submit_evaluation', methods=["POST"])
def submit_evaluation():
    '''
    Creates checkoff evaluation for a student.\n
    Returns created checkoff evaluation\n
    @author sravyabalasa
    '''
    checkoff_id = request.json.get('checkoff_id', None)
    grader_id = request.json.get('grader_id', None)
    student_id = request.json.get('student_id', None)
    score_fract = request.json.get('score_fract', None)

    ce = CheckoffEvaluation.create_eval(checkoff_id, grader_id,
                                        student_id, score_fract)
    checkoff = Checkoff.get_checkoff_by_id(checkoff_id)
    course = Course.get_course_by_id(checkoff.course_id)
    student = User.get_user_by_id(student_id)
    grader = User.get_user_by_id(grader_id)

    msg = f'Hi {student.first_name} {student.last_name}!\n\n'
    msg += 'You\'re getting this automated email because you were'
    msg += f' successfully checked off for {course.short_name}.\n\n'
    msg += f'Assignment: {checkoff.name}\n'
    msg += f'Tutor: {grader.first_name} {grader.last_name}\n'
    msg += f'Score: {ce.score}\n\n'
    msg += 'Please keep this email for future reference.\n'
    msg += 'Please do not reply to this email. If you have any questions '
    msg += 'about this confirmation, '
    msg += 'please contact a member of the course staff.'

    title = f'Checkoff Confirmation for {course.short_name} - {checkoff.name}'

    if MailUtil.get_instance().send(student.email, title, msg):
        Logger.get_instance().custom_msg(f'Email sent to {student.email}', LogLevels.INFO)
        return jsonify({'reason': 'checkoff evaluation successfully created',
                        'eval': ce.to_json()}), 200
    else:
        Logger.get_instance().custom_msg('Emailer failed to send email.', LogLevels.ERR)
        return jsonify({'reason': 'Invalid email address'}), 510



@checkoff_api_bp.route('/get_latest_ce_all_students_for_course',\
                       methods=["GET"])
def get_evaluations_course():
    '''
    Returns latest checkoff evaluation for each student in course.\n
    @author sravyabalasa
    '''
    course_id = request.args.get('course_id', None, type=int)
    checkoff_id = request.args.get('checkoff_id', None, type=int)

    evals = CheckoffEvaluation.\
        find_latest_ce_for_checkoff_for_all_students(course_id, checkoff_id)
    ret = list(map(lambda eval: {'student': eval[0].to_json(),
                                 'eval': eval[1].to_json() if eval[1] is not None else None}, evals))
    return jsonify({'reason': 'checkoff evaluations queried',
                    'evals': ret}), 200


@checkoff_api_bp.route('/get_latest_ce_all_checkoffs_for_student',
                       methods=["GET"])
def get_evaluations_student():
    '''
    Returns latest checkoff evaluations for all checkoffs for student.\n
    @author sravyabalasa
    '''
    course_id = request.args.get('course_id', None, type=int)
    student_id = request.args.get('student_id', None, type=int)

    evals = CheckoffEvaluation.\
        find_latest_ce_for_all_checkoffs_for_student(course_id, student_id)
    ret = list(map(lambda eval: {'checkoff': eval[0].to_json(),
                                 'eval': eval[1].to_json() if eval[1] is not None else None}, evals))
    return jsonify({'reason': 'checkoff evaluations queried',
                    'evals': ret}), 200
