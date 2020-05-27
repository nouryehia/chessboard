from flask_cors import CORS
from flask import Blueprint, request, jsonify
from ..security.roles import role_required, URole
from ..models.course import Course, Quarter

course_api_bp = Blueprint('course_api', __name__)
CORS(course_api_bp, supports_credentials=True)


@course_api_bp.route('/create_course', methods=['POST'])
# @role_required(role=URole.ADMIN.value)
def create_course():
    """
    @author : @mihaivaduva21
    Creates a course, only users with ADMIN role should call this.
    """
    description = request.json['description']
    name = request.json['name']
    quarter = Quarter(int(request.json['quarter'])).value
    short_name = request.json['short_name']
    url = request.json['url'] if 'url' in request.json else None
    year = int(request.json['year'])
    active = bool(request.json['active']) if 'active' in request.json else False
    queue_enabled = bool(request.json['queue_enabled']) if 'queue_enabled' in request.json else False
    cse = bool(request.json['cse']) if 'cse' in request.json else False
    queue_id = int(request.json['queue_id'])

    if Course.create_course(description=description, name=name,
                            quarter=quarter, short_name=short_name, url=url,
                            year=year, active=active,
                            queue_enabled=queue_enabled, cse=cse,
                            queue_id=queue_id) is not None:
        return jsonify({'reason': 'course created'}), 200
    else:
        return jsonify({'reason': 'course existed'}), 300


@course_api_bp.route('/delete_course', methods=['POST'])
# @role_required(role=URole.ADMIN.value)
def delete_course():
    """
    @author : @mihaivaduva21
    """

    quarter = request.json['quarter']
    short_name = request.json['short_name']
    year = request.json['year']

    if Course.delete_course(quarter=quarter, short_name=short_name,
                            year=year) is True:
        return jsonify({'reason': 'course deleted'}), 200
    else:
        return jsonify({'reason': 'course non-existent'}), 300