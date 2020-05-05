from flask_cors import CORS
from flask import Blueprint, request, jsonify
from ..security.roles import role_required, URole
from ..models.course import Course

course_api_bp = Blueprint('course_api', __name__)
CORS(course_api_bp, supports_credentials=True)


@course_api_bp.route('/create_course', methods=['POST'])
@role_required(role=URole.ADMIN.value)
def create_course():
    """
    @author : @mihaivaduva21
    """

    description = request.json['description']
    name = request.json['name'] 
    quarter = request.json['quarter']
    short_name = request.json['short_name']
    url = request.json['url'] if 'url' in request.json else None
    year = request.json['year']
    active = request.json['active'] if 'active' in request.json else False
    queue_enabled = request.json['queue_enabled'] if 'queue_enabled' in request.json else False
    cse = request.json['cse'] if 'cse' in request.json else False
    queue_id = request.json['queue_id']

    if Course.create_course(description=description, name=name,
                            quarter=quarter, short_name=short_name, url=url,
                            year=year, active=active,
                            queue_enabled=queue_enabled, cse=cse,
                            queue_id=queue_id) is not None:
        return jsonify({'reason': 'course created'}), 200
    else:
        return jsonify({'reason': 'course existed'}), 300


@course_api_bp.route('/delete_course', methods=['POST'])
@role_required(role=URole.ADMIN.value)
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