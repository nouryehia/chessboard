from flask_cors import CORS
from flask_login import login_required  # , current_user
from flask import Blueprint, request, jsonify
from ..models.user import User


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

    # Check the authroity of the operation
    # c_u_id = current_user.id
    # ecu = EnrolledCourse.find_user_in_course(user_id=user_id,
    #                                          course_id=course_id)
    # if ecu.get_role() not in [Role.INSTRUCTOR, Role.ROOT, Role.ADMIN]:
    #    return jsonify({'reason': 'Method is forbiden from you'}), 400

    if EnrolledCourse.enroll_user_to(user_id=user_id,
                                     course_id=course_id,
                                     section_id=section_id,
                                     role=Role(role)):
        return jsonify({'reason': 'user enrolled'}), 200
    else:
        return jsonify({'reason': 'user existed'}), 300


@enrolled_course_api_bp.route('/delete_user_from_course', methods=['POST'])
@login_required
def delete_user_from_course():
    """
    The route to remote an user from a particular course.
    """
    user_id = request.json['user_id']
    course_id = request.json['course_id']
    # Check the authroity of the operation
    # c_u_id = current_user.id
    ecu = EnrolledCourse.find_user_in_course(user_id=user_id,
                                             course_id=course_id)
    if ecu.get_role() not in [Role.INSTRUCTOR, Role.ROOT, Role.ADMIN]:
        return jsonify({'reason': 'Method is forbiden from you'}), 400
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
    return jsonify(EnrolledCourse.find_user_in_course(user_id=user_id,
                                                      course_id=course_id))


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
        i = 0
        for ec in ec_list:
            i += 1
            user = User.get_user_by_id(ec)
            scr = {}
            scr['user_info'] = user.to_json()
            scr['enrolled_user_info'] = ec.to_json()
            ret['user' + str(i)] = scr
        return jsonify({'reason': 'success', 'result': ret}), 200
    else:
        return jsonify({'reason': 'course not found'}), 400


@enrolled_course_api_bp.route('/get_user_in_section', methods=['POST'])
@login_required
def get_user_in_section():
    """
    The route to remote an user from a particular course.
    """
    sid = request.json['section_id']
    cid = request.json['course_id']
    ecs = EnrolledCourse.find_all_user_in_section(course_id=cid,
                                                  section_id=sid)
    i = 0
    ret = {}
    for ec in ecs:
        user = User.get_user_by_id(id=ec.user_id)
        i += 1
        scr = {}
        scr['user_info'] = user.to_json()
        scr['enrolled_user_info'] = ec.to_json()
        ret['User' + str(i)] = scr
    return jsonify({'reason': 'success', 'result': ret}), 200


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
    return jsonify(EnrolledCourse.find_user_in_all_course(user_id=user_id,
                                                          role=role))


@enrolled_course_api_bp.route('/find_active_tutor_for', methods=['GET'])
@login_required
def find_active_tutor_for():
    queue_id = request.json['queue_id']
    return jsonify(EnrolledCourse.find_active_tutor_for(queue_id=queue_id))
