#from flask_login import login_required

from ..models.assignment import Assignment

from flask import Blueprint, request, jsonify

assignment_api_bp = Blueprint('assignment_api', __name__)


@assignment_api_bp.route('/create_assignment', methods=['POST'])
#@login_required
def create_assignment():
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
    course_id = request.json['course_id']

    assignments = Assignment.find_all_for_course(course_id)
    if not assignments:
        return jsonify({'reason': 'course does not exist'}), 400
    else:
        ret = list(map(lambda assignment: assignment.to_json(), assignments))
        return jsonify({'reason': 'request OK', 'result': ret}), 200


@assignment_api_bp.route('/delete_assignment_for_course', methods=['PUT'])
def delete_assignment_for_course():
    course_id = request.json['course']
    assignment_id = request.json['assignment']

    ret = Assignment.delete_assignment_for_course(course_id, assignment_id)
    if not ret:
        return jsonify({'reason': 'assignment does not exist'}), 400
    else:
        return jsonify({'reason': 'assignment deleted'}), 200

@assignment_api_bp.route('/delete_all_for_course', methods=['PUT'])
def delete_all_for_course():
    course_id = request.json['course']

    Assignment.delete_all_for_course(course_id)

    return jsonify({'reason': 'assignments deleted'}), 200

@assignment_api_bp.route('/restore_assignment_for_course', methods=['PUT'])
def restore_assignment_for_course():
    course_id = request.json['course']
    assignment_id = request.json['assignment']

    ret = Assignment.restore_assignment_for_course(course_id, assignment_id)
    if not ret:
        return jsonify({'reason': 'assignment does not exist'}), 400
    else:
        return jsonify({'reason': 'assignment restored'}), 200

@assignment_api_bp.route('/restore_all_for_course', methods=['PUT'])
def restore_all_for_course():
    course_id = request.json['course']

    Assignment.restore_all_for_course(course_id)

    return jsonify({'reason': 'assignments restored'}), 200
