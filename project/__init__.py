from flask import jsonify

from .setup import app, login_manager

from .src.models.user import User

# Import routes here
from .src.api.user import user_api_bp as uapi
from .src.api.assignment import assignment_api_bp as aapi
from .src.api.enrolled_course import enrolled_course_api_bp as eapi

app.register_blueprint(uapi, url_prefix="/api/users")
app.register_blueprint(aapi, url_prefix="/api/assignment")
app.register_blueprint(eapi, url_prefix="/api/enroll_course")


def load_user(user_id):
    '''
    Function used to be a default loader for flask login.
    '''
    return User.get_user_by_id(user_id)


login_manager.user_loader(load_user)


def unauthorized():
    '''
    Function used to turn down people who aren't logged in trying to
    access routes that are locked down.
    '''
    return jsonify({'reason': "Not logged in!"}), 403


login_manager.unauthorized_handler(unauthorized)
