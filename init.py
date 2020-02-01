from flask_api import FlaskAPI
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = FlaskAPI(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@database/autograder'
db = SQLAlchemy(app)
db.init_app(app)
