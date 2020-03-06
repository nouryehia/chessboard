from flask_login import login_required, login_user, logout_user

from ..models.user import User

from flask import Blueprint, request, jsonify


user_api_bp = Blueprint('user_api', __name__)


@user_api_bp.route('/login', method=['GET'])
def login():
    email = request.json['email']
    password = request.json['password']
    remember = True if request.json['remember'] == 'true' else False

    if User.check_password(email, password):
        user = User.find_by_pid_email_fallback(None, email)
        user.update_login_timestamp()
        login_user(user, remember=remember)
        return jsonify({'reason': 'logged in'})

@user_api_bp.route('/create_user', methods=['POST'])
def create_user():
    email = request.json['email']
    f_name = request.json['fname']
    l_name = request.json['lname']
    pid = request.json['pid'] if 'pid' in request.json else None
    password = request.json['passwd'] if 'passwd' in request.json else None

    if not User.create_user(email, f_name, l_name, pid, password):
        return jsonify({'reason': 'user exists'}), 300
    else:
        return jsonify({'reason': 'user created'}), 200


@user_api_bp.route('/get_all_users', methods=['GET'])
def get_all():
    res = []
    all_users = User.get_all_users()
    for user in all_users:
        val = {}
        val['first name'] = user.first_name
        val['last name'] = user.last_name
        val['email'] = user.email
        val['id'] = user.id
        val['pid'] = user.pid
        res.append(val)
    return jsonify({'result': res}), 200


@user_api_bp.route('/get_user', methods=['GET'])
def get():
    email = request.json['email']
    pid = request.json['pid'] if 'pid' in request.json else None

    found = User.find_by_pid_email_fallback(pid, email)

    if not found:
        return jsonify({'reason': 'User not found'}), 400
    else:
        res = {}
        res['id'] = found.id
        res['first name'] = found.first_name
        res['last name'] = found.last_name
        res['pid'] = found.pid
        res['email'] = found.email
        return jsonify({'result': res}), 200
