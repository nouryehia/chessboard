from flask_cors import CORS
from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user


from ..models.checkoff import CheckoffSuite, CheckoffEvaluation, Checkoff


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
    points = request.json['points'] if 'points' in request.json else None
    



'''
LIST OF METHODS:
 - 
 - 
'''