from flask_api import FlaskAPI
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask.cli import FlaskGroup

app = FlaskAPI(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
db.init_app(app)
cli = FlaskGroup(app)
login_manager = LoginManager()
current_app = login_manager.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello Queues!'