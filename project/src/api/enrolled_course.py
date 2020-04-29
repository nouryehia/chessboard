from flask_cors import CORS
from flask_login import login_required
from flask import Blueprint, request, jsonify

from ..models.enrolled_course import Role, EnrolledCourse

enrolled_course_api_bp = Blueprint('enrolled_course_api', __name__)
CORS(enrolled_course_api_bp, supports_credentials=True)


@enrolled_course_api_bp.route('/enroll_user', methods=['POST'])
def enroll_user():
    """
    Route to enroll a user in to a specific section of a course.
    When the role field of the request is empty, the default would be student.
    @authoer Yixuan
    """
    user_id = request.json['user_id']
    role = request.json['role'] if 'role' in request.json \
        else Role.STUDENT.value
    section_id = request.json['section_id']
    course_id = request.json['course_id']

    if EnrolledCourse.enroll_user_to(user_id=user_id,
                                     course_id=course_id,
                                     section_id=section_id,
                                     role=Role(role)):
        return jsonify({'reason': 'user enrolled'}), 200
    else:
        return jsonify({'reason': 'user existed'}), 400


@enrolled_course_api_bp.route('/delete_user_from_course', methods=['POST'])
@login_required
def delete_user_from_course():
    """
    The route to remote an user from a particular course.
    """
    user_id = request.json['user_id']
    course_id = request.json['course_id']
    if EnrolledCourse.delete_enrolled_user_from_course(user_id=user_id,
                                                       course_id=course_id):
        return jsonify({'reason': 'user deleted'}), 200
    else:
        return jsonify({'reason': 'user not found'}), 400


@enrolled_course_api_bp.route('/get_user_in_course', methods=['GET'])
@login_required
def get_user_of_course():
    """
    Route to get a user from a specific course.
    """
    user_id = request.json['user_id']
    course_id = request.json['course_id']
    ec_enrty = EnrolledCourse.find_user_in_course(user_id=user_id,
                                                  course_id=course_id)
    if ec_enrty:
        return jsonify({'reason': 'success', 'result': ec_enrty}), 200
    else:
        return jsonify({'reason': 'user not enrolled in course'}), 400


@enrolled_course_api_bp.route('/get_all_user_in_course', methods=['GET'])
@login_required
def get_all_user():
    """
    Route to get all the users of that is in a given course.
    """
    course_id = request.json['course_id']
    status, ec_list = EnrolledCourse.\
        find_all_user_in_course(course_id=course_id)
    if status:
        ret = {}
        ret = {}
        i = 0
        for ec in ec_list:
            i += 1
            ret['user' + str(i)] = ec.to_json
        return jsonify({'reason': 'success', 'result': ret}), 200
    else:
        return jsonify({'reason': 'course not found'}), 400


@enrolled_course_api_bp.route('/get_user_in_all_course',
                              methods=['GET'])
@login_required
def get_user_in_all_course():
    """
    Route to get all the courses that a user is in.
    There can be a role being specified, if not,
    all the courses will be returned regardless of the role.
    """
    user_id = request.json['user_id']
    role = request.json['role'] if 'role' in request else None
    ec_entries = EnrolledCourse.find_user_in_all_course(user_id=user_id,
                                                        role=role)
    return jsonify({'reason': 'success', 'result': ec_entries}), 200


@enrolled_course_api_bp.route('/find_active_tutor_for', methods=['GET'])
@login_required
def find_active_tutor_for():
    qid = request.json['queue_id']
    status, reason, at = EnrolledCourse.find_active_tutor_for(queue_id=qid)
    if status:
        return jsonify({'reason': reason, 'result': at}), 200
    else:
        return jsonify({'reason': reason}), 400
