from flask_cors import CORS
from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user

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
    Route used to update an existiing checkoff in the database. Returns
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
