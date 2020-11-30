from flask_api import FlaskAPI
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask.cli import FlaskGroup
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

app = FlaskAPI(__name__)
CORS(app)

# Have cookie sent
#app.config["SECURITY_CSRF_COOKIE"] = {"key": "XSRF-TOKEN"}
# Don't have csrf tokens expire (they are invalid after logout)
#app.config["WTF_CSRF_TIME_LIMIT"] = None
# You can't get the cookie until you are logged in.
#app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True
csrf = CSRFProtect()
csrf.init_app(app)

app.config.from_object("project.config.Config")

db = SQLAlchemy(app)
db.init_app(app)

cli = FlaskGroup(app)

login_manager = LoginManager()
login_manager.init_app(app)
