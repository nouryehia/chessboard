from flask_api import FlaskAPI
from flask_cors import CORS

app = FlaskAPI(__name__)
CORS(app)


@app.route('/')
def hello():
    return {'sup': 'dude'}


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
