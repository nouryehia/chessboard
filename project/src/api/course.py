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
    req = request.get_json()
    description = req['description']
    name = req['name']
    quarter = Quarter[req['quarter']].value
    short_name = req['short_name']
    url = req['url'] if 'url' in req else None
    year = int(req['year'])
    active = bool(req['active'])
    queue_enabled = bool(req['queue_enabled']) if 'queue_enable' in req else False
    cse = bool(req['cse']) if 'cse' in req else False
    queue_id = req['queue_id'] if 'queue_id' in req else None

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
    quarter = Quarter[str(request.json['quarter'])].value
    short_name = str(request.json['short_name'])
    year = int(request.json['year'])

    if Course.delete_course(quarter=quarter, short_name=short_name,
                            year=year) is True:
        return jsonify({'reason': 'course deleted'}), 200
    else:
        return jsonify({'reason': 'course non-existent'}), 300


@course_api_bp.route('/find_course_by_id', methods=['GET'])
def find_course_by_id():
    """
    @author: @sccontre
    """
    id = request.args.get('id', type=int)
    c = Course.get_course_by_id(id)
    if c is None:
        return jsonify({'reason': 'course not found'}), 400
    else:
        return jsonify({'reason': 'course found', 'result': c.to_json()}), 200


@course_api_bp.route('/find_all_courses', methods=['GET'])
def find_all_courses():
    """
    @author: YixuanZ
    """
    try:
        q = Quarter[request.args.get('quarter', type=str)].value
    except KeyError:
        q = None
    y = request.args.get('year', type=int)
    crs = Course.get_all_courses(quarter=q, year=y)
    crs = list(map(lambda x: x.to_json(), crs))
    return jsonify({'reason': 'successed', 'result': crs}), 200
