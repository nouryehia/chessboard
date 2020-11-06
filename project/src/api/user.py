from flask_cors import CORS
from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user


from ..models.user import User
from ..utils.mailer import MailUtil
from ..utils.logger import Logger, LogLevels


user_api_bp = Blueprint('user_api', __name__)
CORS(user_api_bp, supports_credentials=True)


@user_api_bp.route('/login', methods=['POST'])
def login():
    '''
    Route used to log in a user. Creates a session for them and returns the
    user object.\n
    @author npcompletenate
    '''
    email = request.json.get('email', None)
    password = request.json.get('password', '')
    remember = True if request.json.get('remember', '') == 'true' else False

    if User.check_password(email, password):
        user = User.find_by_pid_email_fallback(None, email)
        user.update_login_timestamp()
        Logger.get_instance().logged_in(user)
        login_user(user, remember=remember)
        return jsonify({'reason': 'logged in', 'result': user.to_json()})
    else:
        return jsonify({'reason': 'User/Password doesn\'t match'}), 400


@user_api_bp.route('/logout', methods=['POST'])
#@login_required
def logout():
    '''
    Route used to log out a user. Ends their session.\n
    @author npcompletenate
    '''
    logout_user()
    return jsonify({'reason': 'request OK'}), 200


@user_api_bp.route('/reset_password', methods=['PUT'])
#@login_required
def reset_password():

    id = request.json.get('id', None)
    passwd = request.json.get('password', None)
    old_pass = request.json.get('old_password', None)

    user = User.get_user_by_id(id)
    if User.check_password(user.email, old_pass):
        user.reset_password(passwd)
        Logger.get_instance().reset_password(user.email)
        msg = 'Hi there!\nYou\'re getting this email because you' +\
            ' reset your password. If this wasn\'t you, contact someone' +\
            ' on the Autograder team IMMEDIATELY.\nPlease do not reply to' +\
            ' this email; replies are not checked.' +\
            '\n\nCheers,\nThe Autograder Team'
        if MailUtil.get_instance().send(user.email, 'Password Reset', msg):
            Logger.get_instance().custom_msg(f'Email sent to {user.email}', LogLevels.INFO)
            return jsonify({'reason': 'request OK'}), 200
        else:
            Logger.get_instance().custom_msg('Emailer failed to send email.', LogLevels.ERR)
            return jsonify({'reason': 'Invalid email address'}), 510
    else:
        return jsonify({'reason': 'Old password doesn\'t match'}), 400


@user_api_bp.route('/forgot_password', methods=['PUT'])
def forgot_password():
    user = User.find_by_pid_email_fallback(None, request.json.get('email', None))
    if user:
        new_pass = user.create_random_password()
        Logger.get_instance().forgot_password(user.email)
        msg = 'Hi there!\nYou\'re getting this email because you' +\
            ' forgot your password. If this wasn\'t you, contact someone' +\
            ' on the Autograder team IMMEDIATELY.\nPlease do not reply to' +\
            ' this email; replies are not checked.' +\
            f' Your temp password is {new_pass}; go change it ASAP!' +\
            '\n\nCheers,\nThe Autograder Team'

        if MailUtil.get_instance().send(user.email, 'Forgot Password', msg):
            Logger.get_instance().custom_msg(f'Email sent to {user.email}', LogLevels.INFO)
            return jsonify({'reason': 'request OK'}), 200
        else:
            Logger.get_instance().custom_msg('Emailer failed to send email.', LogLevels.ERR)
            return jsonify({'reason': 'Invalid email address'}), 510
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
    email = request.json.get('email')
    f_name = request.json.get('fname')
    l_name = request.json.get('lname')
    pid = request.json.get('pid', None)
    password = request.json.get('passwd', None)

    status, pwd, user = User.create_user(email, f_name, l_name, pid, password)
    if not status:
        Logger.get_instance().create_user_exist(email)
        return jsonify({'reason': 'user exists'}), 300
    else:
        res = False if password else True
        Logger.get_instance().create_user(user)

        msg = 'Hi there!\nYou\'re getting this email because an' +\
            ' Autograder account was created for you.'

        if res:
            msg += '\nA temporary password was created for you, so go change '
            msg += f'it! Your temporary password is {pwd}.'
        else:
            msg += 'You set your password when you created, so try logging in!'

        msg += '\n\nCheers,\nThe Autograder Team'

        if MailUtil.get_instance().send(user.email, 'Created Autograder Account', msg):
            Logger.get_instance().custom_msg(f'Email sent to {user.email}', LogLevels.INFO)
        else:
            Logger.get_instance().custom_msg('Emailer failed to send email.', LogLevels.ERR)
        ret = {'reason': 'user created', 'password generated': res}
        return jsonify(ret), 200


@user_api_bp.route('/get_all_users', methods=['GET'])
#@login_required
def get_all():
    '''
    Route used to get all users in the DB. Probably won't be used
    much since it wouldn't be too useful to get potentially thousands
    of records simulataneously.
    @author npcompletenate
    '''
    Logger.get_instance().custom_msg('get_all_users route run', LogLevels.WARN)
    res = list(map(lambda user: user.to_json(), User.get_all_users()))
    return jsonify({'reason': 'request OK', 'result': res}), 200


@user_api_bp.route('/get_user', methods=['GET'])
#@login_required
def get():
    '''
    Route used to get a particular user. We try to find by PID first,
    searching by email if we cannot find a user with that particular PID.\n
    '''
    email = request.args.get('email', None, type=str)
    pid = request.args.get('pid', None)

    found = User.find_by_pid_email_fallback(pid, email)

    if not found:
        return jsonify({'reason': 'User not found'}), 400
    else:
        ret = {'reason': 'request OK', 'result': found.to_json()}
        return jsonify(ret), 200


@user_api_bp.route('/update_user', methods=['PUT'])
#@login_required
def update_user():
    '''
    Update user's information at user's discretion\n
    '''
    id = request.json.get('id', None)
    f_name = request.json.get('fname', '')

    user = User.get_user_by_id(id)
    if user:
        user.update_user(f_name)

        ret = {'reason': 'User successfully updated', 'result': user.to_json()}
        return jsonify(ret), 200
    else:
        ret = {'reason': 'User not found', 'result': {}}
        return jsonify(ret), 400


@user_api_bp.route('/check_password', methods=['POST'])
#@login_required
def check_password():
    '''
    Check if the user's password matches the given in the database\n
    '''
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    match = User.check_password(email, password)

    if match:
        return jsonify({'reason': 'Passwords match'}), 200
    else:
        return jsonify({'reason': 'Passwords do not match'}), 400
