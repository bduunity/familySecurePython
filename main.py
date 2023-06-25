from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    emit('my response', json)


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('server_response', {'data': 'Welcome!'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='192.168.1.6', port=5000, allow_unsafe_werkzeug=True)
