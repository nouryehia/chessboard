from flask_cors import CORS
from flask import Blueprint, request, jsonify

from ..models.checkoff import CheckoffEvaluation, Checkoff


checkoff_api_bp = Blueprint('user_api', __name__)
CORS(checkoff_api_bp, supports_credentials=True)


@checkoff_api_bp.route('/create_checkoff', methods=['POST'])
def create_checkoff():
    '''
    Route used to create a new checkoff. Creates a checkoff and returns
    the checkoff object.\n
    @author sravyabalasa
    '''
    description = request.json['description'] if 'description' in request.json else None
    name = request.json['name'] if 'name' in request.json else None
    course_id = request.json['course_id'] if 'course_id' in request.json else None
    points = request.json['points'] if 'points' in request.json else None
    status = request.json['status'] if 'status' in request.json else None

    checkoff = Checkoff.create_checkoff(description, name, course_id, points, status)

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
    id = request.json['id'] if 'id' in request.json else None
    description = request.json['description'] if 'description' in request.json else None
    name = request.json['name'] if 'name' in request.json else None
    points = request.json['points'] if 'points' in request.json else None    
    status = request.json['status'] if 'status' in request.json else None

    checkoff = Checkoff.get_checkoff_by_id(id)
    checkoff.update_checkoff(description, name, points)

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
    @sravyabalasa
    '''
    id = request.json['id'] if 'id' in request.json else None

    checkoff = Checkoff.get_checkoff_by_id(id)
    checkoff.soft_delete()

    return jsonify({'reason': 'checkoff successfully deleted',
                    'checkoff': checkoff.to_json()}), 200


@checkoff_api_bp.route('/submit_evaluation', methods=["POST"])
def submit_evaluation():
    '''
    Creates checkoff evaluation for a student.\n
    Returns created checkoff evaluation\n
    @sravyabalasa
    '''
    checkoff_id = request.json['checkoff_id']
    grader_id = request.json['grader_id']
    student_id = request.json['student_id']
    score_fract = request.json['score_fract']

    ce = CheckoffEvaluation.create_eval(checkoff_id, grader_id, student_id, score_fract)

    return jsonify({'reason': 'checkoff evaluation successfully created',
                    'eval': ce.to_json()}), 200


@checkoff_api_bp.route('/get_latest_ce_all_students_for_course', methods=["GET"])
def get_evaluations_course():
    '''
    Returns latest checkoff evaluation for each student in course.\n
    @sravyabalasa
    '''
    course_id = request.args.get('course_id')
    checkoff_id = request.args.get('checkoff_id')

    evals = CheckoffEvaluation.find_latest_ce_for_checkoff_for_all_students(course_id, checkoff_id)
    ret = list(map(lambda eval: {'student': eval[0].to_json, 'eval': eval[1].to_json()}, evals))
    return jsonify({'reason': 'checkoff evaluations queried',
                    'evals': ret}), 200


@checkoff_api_bp.route('/get_latest_ce_all_checkoffs_for_student', methods=["GET"])
def get_evaluations_student():
    '''
    Returns latest checkoff evaluations for all checkoffs for student.\n
    @sravyabalasa
    '''
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    evals = CheckoffEvaluation.find_latest_ce_for_all_checkoffs_for_student(course_id, student_id)
    ret = list(map(lambda eval: eval.to_json(), evals))
    return jsonify({'reason': 'checkoff evaluations queried',
                    'evals': ret}), 200
