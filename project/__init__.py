from flask import jsonify

from .setup import app, login_manager

from .src.models.user import User

# ----------------------------------------------------------------
# DO NOT EDIT ABOVE THE LINE

# Import routes here
from .src.api.user import user_api_bp as uapi
from .src.api.ticket import ticket_api_bp as tapi
from .src.api.assignment import assignment_api_bp as aapi
from .src.api.enrolled_course import enrolled_course_api_bp as eapi
from .src.api.queue import queue_api_bp as qapi
from .src.api.news_feed import newsfeed_api_bp as nfapi
from .src.api.course import course_api_bp as capi
from .src.api.section import section_api_bp as sapi
from .src.api.checkoff import checkoff_api_bp as chapi

app.register_blueprint(uapi, url_prefix="/api/users")
app.register_blueprint(tapi, url_prefix="/api/ticket")
app.register_blueprint(aapi, url_prefix="/api/assignment")
app.register_blueprint(eapi, url_prefix="/api/enroll_course")
app.register_blueprint(qapi, url_prefix="/api/queue")
app.register_blueprint(nfapi, url_prefix="/api/newsfeeds")
app.register_blueprint(capi, url_prefix="/api/course")
app.register_blueprint(sapi, url_prefix="/api/section")
app.register_blueprint(chapi, url_prefix="/api/checkoff")

# DO NOT EDIT BELOW THE LINE
# ----------------------------------------------------------------


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
