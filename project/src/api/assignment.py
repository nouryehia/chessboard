from flask_cors import CORS
from flask_login import login_required
from flask import Blueprint, request, jsonify

from ..models.assignment import Assignment

assignment_api_bp = Blueprint('assignment_api', __name__)
CORS(assignment_api_bp, supports_credentials=True)


@assignment_api_bp.route('/create_assignment', methods=['POST'])
#@login_required
def create_assignment():
    '''
    Route used to create an assignment in the DB. Only accepts post requests.
    Takes in due date, name, category id, course id, checkoff suite id, and
    percent worth of assignment in course.
    @author tiffany-meng
    '''
    due = request.json['due']
    name = request.json['name']
    category = request.json['category']
    course = request.json['course']
    checkoff_suite = request.json['csuite']
    percent = request.json['percent']

    Assignment.create_assignment(due, name, category,
                                 course, checkoff_suite, percent)

    return jsonify({'reason': 'assignment_created'}), 200


@assignment_api_bp.route('/get_assignments_for_course', methods=['GET'])
#@login_required
def get_assignments_for_course():
    '''
    Route used to retrieve all assignments for a specific course. Will
    check if course exists first.
    @author tiffany-meng
    '''
    course_id = request.json['course_id']

    '''
    crs = Course.find_by_id(course_id)
    if not crs:
        return jsonify({'reason': 'course does not exist}), 400
    else:
    TODO: wait for Course model merge
    '''

    assignments = Assignment.find_all_for_course(course_id)
    ret = list(map(lambda assignment: assignment.to_json(), assignments))
    return jsonify({'reason': 'request OK', 'result': ret}), 200


@assignment_api_bp.route('/delete_assignment_for_course', methods=['PUT'])
#@login_required
def delete_assignment_for_course():
    '''
    Route that deletes a specific assignment for a couse. Needs the id of
    the course and the id of the assignment.
    @author tiffany-meng
    '''
    course_id = request.json['course']
    assignment_id = request.json['assignment']

    '''
    crs = Course.find_by_id(course_id)
    if not crs:
        return jsonify({'reason': 'course does not exist}), 400
    else:
    TODO: wait for Course model merge
    '''

    ret = Assignment.delete_asn_for_course(course_id, assignment_id)
    if not ret:
        return jsonify({'reason': 'assignment does not exist'}), 400
    else:
        return jsonify({'reason': 'assignment deleted'}), 200


@assignment_api_bp.route('/delete_all_for_course', methods=['PUT'])
#@login_required
def delete_all_for_course():
    '''
    Route that deletes all assignments for a couse. Needs the id
    of the course and the id of the assignment.
    @author tiffany-meng
    '''
    course_id = request.json['course']

    '''
    crs = Course.find_by_id(course_id)
    if not crs:
        return jsonify({'reason': 'course does not exist}), 400
    else:
    TODO: wait for Course model merge
    '''

    Assignment.delete_all_for_course(course_id)

    return jsonify({'reason': 'assignments deleted'}), 200


@assignment_api_bp.route('/restore_assignment_for_course', methods=['PUT'])
#@login_required
def restore_assignment_for_course():
    '''
    Route that restores a specific assignment for a course. Needs a course
    id and an assignment id.
    @author tiffany-meng
    '''
    course_id = request.json['course']
    assignment_id = request.json['assignment']

    '''
    crs = Course.find_by_id(course_id)
    if not crs:
        return jsonify({'reason': 'course does not exist}), 400
    else:
    TODO: wait for Course model merge
    '''

    ret = Assignment.restore_asn_for_course(course_id, assignment_id)
    if not ret:
        return jsonify({'reason': 'assignment does not exist'}), 400
    else:
        return jsonify({'reason': 'assignment restored'}), 200


@assignment_api_bp.route('/restore_all_for_course', methods=['PUT'])
#@login_required
def restore_all_for_course():
    '''
    Route that restores all assignments for a course. Needs a course
    id and an assignment id.
    @author tiffany-meng
    '''
    course_id = request.json['course']

    '''
    crs = Course.find_by_id(course_id)
    if not crs:
        return jsonify({'reason': 'course does not exist}), 400
    else:
    TODO: wait for Course model merge
    '''

    Assignment.restore_all_for_course(course_id)

    return jsonify({'reason': 'assignments restored'}), 200

