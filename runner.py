from project.setup import cli
from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(msg):
    print('received msg: ' + msg)
    send(msg, broadcast=True)
    return None


# This is all we need to get it goin
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0',debug=True, port=5000)
    cli()
