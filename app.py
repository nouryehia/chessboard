from flask_api import FlaskAPI
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = FlaskAPI(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:woshishabi2333@localhost/autograder'
db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def hello():
    return {'sup': 'dude'}


if __name__ == '__main__':
    db.create_all()
    app.run('0.0.0.0', 5000, debug=True)
