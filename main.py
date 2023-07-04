import json

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

app.config['MYSQL_HOST'] = '83.136.233.166'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aa@71077431'
app.config['MYSQL_DB'] = 'taxi'

mysql = MySQL(app)


@socketio.on('my event')
def handle_my_custom_event(jsonn):
    print('received json: ' + str(jsonn))
    json_obj = json.loads(jsonn)
    data = json_obj['data']
    print('received data:', data)
    emit('server_response', jsonn)


@socketio.on('register')
def handle_my_custom_event(jsonn):
    print('received json: ' + str(jsonn))
    json_obj = json.loads(jsonn)
    email = json_obj['email']
    password = json_obj['password']
    print('Register:', email, password)

    print('Get data from MySQL')
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users''')
    rows = cur.fetchall()
    for row in rows:
        print(f'{row}')
    cur.close()


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('server_response', {'data': 'Welcome!'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='192.168.1.139', port=5000, allow_unsafe_werkzeug=True)
