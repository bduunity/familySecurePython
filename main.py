import json
import random

from flask import Flask, render_template
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

app.config['MYSQL_HOST'] = '83.136.233.166'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aa@71077431'
app.config['MYSQL_DB'] = 'fsecure'

mysql = MySQL(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'araxmatjonn@gmail.com'
app.config['MAIL_PASSWORD'] = 'iyuqbznfpgilimpv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@socketio.on('message')
def handle_my_custom_event(jsonn):
    print('received json: ' + str(jsonn))
    json_obj = json.loads(jsonn)
    data = json_obj['data']
    print('received data:', data)


@socketio.on('register')
def handle_my_custom_event(jsonn):
    print('received json: ' + str(jsonn))
    json_obj = json.loads(jsonn)
    email = json_obj['email']
    password = json_obj['password']
    print('Register:', email, password)

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cur.fetchone()
    if account:
        print('Error: Email already exists!')
        cur.close()
        emit('register_response', {'message': 'Error: Email already exists!'})
    else:
        # If account doesn't exist, add to database
        # cur.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
        # mysql.connection.commit()
        # cur.close()
        # print('Registration successful!')

        msg = Message('Hello', sender='araxmatjonn@gmail.com', recipients=[email])
        code = generate_five_digit_number()
        msg.body = "Your code: " + str(code)
        mail.send(msg)
        print("Message sent!")
        emit('register_response', {'message': 'Confirm your Email!'})
        cur.execute('INSERT INTO confirm_email (email, code) VALUES (%s, %s)', (email, code))
        mysql.connection.commit()
        cur.close()
        print('Registration successful!')

    # print('Get data from MySQL')
    # cur = mysql.connection.cursor()u
    # cur.execute('''SELECT * FROM users''')
    # rows = cur.fetchall()
    # for row in rows:
    #     print(f'{row}')
    # cur.close()


@socketio.on('email_confirm')
def handle_my_custom_event(jsonn):
    print('received json: ' + str(jsonn))

    json_obj = json.loads(jsonn)
    email = json_obj['email']
    email_code = json_obj['email_code']

    cur = mysql.connection.cursor()
    cur.execute('SELECT code FROM confirm_email WHERE email = %s', email)
    result = cur.fetchone()

    if result is not None and result[0] == email_code:
        emit('register_response', {'message': 'Error: Email already exists!'})

    print('received data:', email, email_code)


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('server_response', {'data': 'Welcome!'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def generate_five_digit_number():
    return random.randint(10000, 99999)


if __name__ == '__main__':
    socketio.run(app, host='192.168.1.139', port=5000, allow_unsafe_werkzeug=True)
