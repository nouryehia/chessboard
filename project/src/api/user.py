from flask_login import login_required, login_user, logout_user

from ..models.user import User

from flask import Blueprint, request, jsonify


user_api_bp = Blueprint('user_api', __name__)


@user_api_bp.route('/login', methods=['POST'])
def login():
    '''
    Route used to log in a user. Creates a session for them and returns the
    user object.\n
    @author npcompletenate
    '''
    email = request.json['email']
    password = request.json['password']
    remember = True if 'remember' in request.json and \
        request.json['remember'] == 'true' else False

    if User.check_password(email, password):
        user = User.find_by_pid_email_fallback(None, email)
        user.update_login_timestamp()
        login_user(user, remember=remember)
        return jsonify({'reason': 'logged in', 'result': user.to_json()})
    else:
        return jsonify({'reason': 'User/Password doesn\'t match'}), 400


@user_api_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    '''
    Route used to log out a user. Ends their session.\n
    @author npcompletenate
    '''
    logout_user()
    return jsonify({'reason': 'request OK'}), 200


@user_api_bp.route('/reset_password', methods=['POST'])
@login_required
def reset_password():
    email = request.json['email']
    passwd = request.json['password']
    old_pass = request.json['old password']

    if User.check_password(email, old_pass):
        user = User.find_by_pid_email_fallback(None, email)
        user.reset_password(passwd)
        return jsonify({'reason': 'request OK'}), 200
    else:
        return jsonify({'reason': 'Old password doesn\'t match'}), 400


@user_api_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    user = User.find_by_pid_email_fallback(None, request.json['email'])
    if user:
        new_pass = user.create_random_password()
        # TODO: send the email here
        return jsonify({'reason': 'request OK'}), 200
    else:
        return jsonify({'reason': 'User not found'}), 400


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

    status, pwd = User.create_user(email, f_name, l_name, pid, password)
    if not status:
        return jsonify({'reason': 'user exists'}), 300
    else:
        res = False if password else True

        if res:
            # TODO need to email out the password we generate
            # if we generate one
            pass
        ret = {'reason': 'user created', 'password generated': res}
        return jsonify(ret), 200


@user_api_bp.route('/get_all_users', methods=['GET'])
@login_required
def get_all():
    '''
    Route used to get all users in the DB. Probably won't be used
    much since it wouldn't be too useful to get potentially thousands
    of records simulataneously.
    @author npcompletenate
    '''
    res = list(map(lambda user: user.to_json(), User.get_all_users()))
    return jsonify({'reason': 'request OK', 'result': res}), 200


@user_api_bp.route('/get_user', methods=['GET'])
@login_required
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
