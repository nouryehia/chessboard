from ..models.user import User

from flask import Blueprint, request, jsonify


user_api_bp = Blueprint('user_api', __name__)


@user_api_bp.route('/create_user', methods=['POST'])
def create_user():
    email = request.json['email']
    f_name = request.json['fname']
    l_name = request.json['lname']
    pid = request.json['pid']
    password = request.json['passwd'] if 'passwd' in request.json else None

    if not User.create_user(email, f_name, l_name, pid, password):
        return jsonify({'reason': 'user exists'}), 300
    else:
        return jsonify({'reason': 'user created'}), 200


@user_api_bp.route('/get_all_users', methods=['GET'])
def get_all():
    return jsonify({'result': User.get_all_users()}), 200


@user_api_bp.route('/get_user', methods=['GET'])
def get():
    email = request.json['email']
    pid = request.json['pid']

    res = User.find_by_pid_with_email_fallback(pid, email)

    if not res:
        return jsonify({'reason': 'User not found'}), 400
    else:
        return jsonify({'result': res}), 200
