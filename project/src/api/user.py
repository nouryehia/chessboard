from ..models.user import User

from flask import Blueprint, request, jsonify


user_api_bp = Blueprint('user_api', __name__)


@user_api_bp.route('/create_user', methods=['POST'])
def create_user():
    '''
    Route used to create a new user in the DB. Only accepts POST requests.\n
    The `pid` field and the `passwd` field do not have to be present in the
    body of the POST request. If no password is provided, we generate one for
    the user.
    @author npcompletenate
    '''
    email = request.json['email']
    f_name = request.json['fname']
    l_name = request.json['lname']
    pid = request.json['pid'] if 'pid' in request.json else None
    password = request.json['passwd'] if 'passwd' in request.json else None

    if not User.create_user(email, f_name, l_name, pid, password):
        return jsonify({'reason': 'user exists'}), 300
    else:
        res = False if password else True
        ret = {'reason': 'user created', 'password generated': res}
        return jsonify(ret), 200


@user_api_bp.route('/get_all_users', methods=['GET'])
def get_all():
    '''
    Route used to get all users in the DB. Probably won't be used
    much since it wouldn't be too useful to get potentially thousands
    of records simulataneously.
    @author npcompletenate
    '''
    res = []
    all_users = User.get_all_users()
    for user in all_users:
        res.append(user.to_json())
    return jsonify({'reason': 'request OK', 'result': res}), 200


@user_api_bp.route('/get_user', methods=['GET'])
def get():
    '''
    Route used to get a particular user. We try to find by PID first,
    searching by email if we cannot find a user with that particular PID.\n
    '''
    email = request.json['email'] if 'email' in request.json else None
    pid = request.json['pid'] if 'pid' in request.json else None

    found = User.find_by_pid_email_fallback(pid, email)

    if not found:
        return jsonify({'reason': 'User not found'}), 400
    else:
        ret = {'reason': 'request OK', 'result': found.to_json()}
        return jsonify(ret), 200
