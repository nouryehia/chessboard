from flask_api import FlaskAPI
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask.cli import FlaskGroup

app = FlaskAPI(__name__)
app.config.from_object("project.config.Config")
CORS(app)
db = SQLAlchemy(app)
db.init_app(app)
cli = FlaskGroup(app)
login_manager = LoginManager()
login_manager.init_app(app)
