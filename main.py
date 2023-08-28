import base64
import json
import random

from flask import Flask, render_template
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL
import secrets

import psycopg2
import secrets
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'corei7'
# app.config['MYSQL_DB'] = 'fsecure'
#
# mysql = MySQL(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:corei7@localhost/FamilySecure'
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'araxmatjonn@gmail.com'
app.config['MAIL_PASSWORD'] = 'iyuqbznfpgilimpv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@socketio.on('save_sms')
def handle_my_custom_event_child_auth_check(jsonn):
    encoded_string = jsonn
    decoded_json_string = base64.b64decode(encoded_string).decode('utf-8')
    data = json.loads(decoded_json_string)
    deviceImei = data["deviceImei"]
    code = data["code"]

    print(deviceImei)
    print(code)

    # cur = mysql.connection.cursor()
    # cur.execute('SELECT deviceImei, code FROM confirm_child WHERE code = %s', (code,))
    # result = cur.fetchone()
    # cur.close()

    result = db.session.query(ConfirmChild).filter_by(code=code).first()

    if result is not None and str(result[1]).strip() == code:
        emit('child_auth_check_response', {'status': True})
    else:
        emit('child_auth_check_response', {'status': False})


@socketio.on('child_auth_check')
def handle_my_custom_event_child_auth_check(jsonn):
    encoded_string = jsonn
    decoded_json_string = base64.b64decode(encoded_string).decode('utf-8')
    data = json.loads(decoded_json_string)
    deviceImei = data["deviceImei"]
    code = data["code"]

    print(deviceImei)
    print(code)

    # cur = mysql.connection.cursor()
    # cur.execute('SELECT deviceImei, code FROM confirm_child WHERE code = %s', (code,))
    # result = cur.fetchone()
    # cur.close()

    result = db.session.query(ConfirmChild).filter_by(code=code).first()

    if result is not None and str(result[1]).strip() == code:
        emit('child_auth_check_response', {'status': True})
    else:
        emit('child_auth_check_response', {'status': False})


@socketio.on('child_auth')
def handle_my_custom_event_add_child(jsonn):
    encoded_string = jsonn
    decoded_json_string = base64.b64decode(encoded_string).decode('utf-8')
    data = json.loads(decoded_json_string)
    deviceImei = data["deviceImei"]
    code = data["code"]

    # cur = mysql.connection.cursor()
    # cur.execute('INSERT INTO confirm_child (deviceImei, code) VALUES (%s, %s)',
    #             (deviceImei, code))
    # mysql.connection.commit()
    # cur.close()

    new_entry = ConfirmChild(deviceimei=deviceImei, code=code)
    db.session.add(new_entry)
    db.session.commit()

    print(deviceImei)
    print(code)


@socketio.on('add_child')
def handle_my_custom_event_add_child(jsonn):
    print('received json: ' + str(jsonn))

    json_obj = json.loads(jsonn)
    code = json_obj['code']
    email = json_obj['email']

    # cur = mysql.connection.cursor()
    # cur.execute('SELECT deviceImei, code FROM confirm_child WHERE code = %s', (code,))
    # result = cur.fetchone()
    # cur.close()

    confirm_child_entry = ConfirmChild.query.filter_by(code=code).first()

    if confirm_child_entry is not None and confirm_child_entry.code.strip() == code:

        # cur_id = mysql.connection.cursor()
        # cur_id.execute('SELECT id FROM users WHERE email = %s ', (email,))
        # result_id = cur_id.fetchone()
        # parent_id = result_id[0]
        # cur_id.close()

        parent_entry = Users.query.filter_by(email=email).first()
        parent_id = parent_entry.id

        db.session.delete(confirm_child_entry)
        db.session.commit()

        new_child = Childs(deviceimei=confirm_child_entry.deviceImei, parent_id=parent_id, name="Child")
        db.session.add(new_child)
        db.session.commit()

        emit('add_child_response', {'message': 'Child Added!', 'status': True})

    else:
        emit('add_child_response', {'message': 'Incorrect Code!', 'status': False})

    #     result_code = str(result[1]).strip()
    #     result_deviceImei = result[0]
    #     print(result_code, result_deviceImei)
    #
    #     if result_code == code:
    #         cur = mysql.connection.cursor()
    #         cur.execute('DELETE FROM confirm_child WHERE code = %s', (code,))
    #         mysql.connection.commit()  # Don't forget to commit the changes
    #         cur.close()
    #         cur = mysql.connection.cursor()
    #         cur.execute('INSERT INTO childs (deviceImei, parent_id, name) VALUES (%s, %s, %s)',
    #                     (result_deviceImei, parent_id, "Child"))
    #         mysql.connection.commit()
    #         cur.close()
    #
    #         emit('add_child_response', {'message': 'Child Added!', 'status': True})
    #
    #     else:
    #         emit('add_child_response', {'message': 'Incorrect Code!', 'status': False})
    # else:
    #     emit('add_child_response', {'message': 'Incorrect Code!', 'status': False})


@socketio.on('get_child_list')
def get_child_list(jsonn):
    print('received json: ' + str(jsonn))

    json_obj = json.loads(jsonn)
    email = json_obj['email']

    # cur = mysql.connection.cursor()
    # cur.execute('SELECT id FROM users WHERE email = %s ', (email,))
    # result_id = cur.fetchone()
    # cur.close()

    user = Users.query.filter_by(email=email).first()

    if user is not None:
        # Using SQLAlchemy to get the child names
        child_entries = Childs.query.filter_by(parent_id=user.id).all()
        if child_entries:
            result_child_names = [child.name for child in child_entries]
            emit('get_child_list_result', {'message': result_child_names})
        else:
            print("not found")
            result_child_names = ["Children Not Found"]  # Setting the default value
            emit('get_child_list_result', {'message': result_child_names})

    # if result_id is not None:
    #     cur = mysql.connection.cursor()
    #     cur.execute('SELECT name FROM childs WHERE parent_id = %s ', (result_id[0],))
    #     result_child_names = cur.fetchall()
    #     cur.close()
    #     print(result_child_names)
    #
    #     if result_child_names is not None and len(result_child_names) > 0:
    #         emit('get_child_list_result', {'message': result_child_names})
    #     else:
    #         print("not found")
    #         result_child_names = [("Children Not Found",)]  # Setting the default value
    #         emit('get_child_list_result', {'message': result_child_names})


@socketio.on('message')
def handle_my_custom_event_message(jsonn):
    print('received json: ' + str(jsonn))
    json_obj = json.loads(jsonn)
    data = json_obj['data']
    print('received data:', data)


@socketio.on('register')
def handle_my_custom_event_register(jsonn):
    print('received json: ' + str(jsonn))
    json_obj = json.loads(jsonn)
    email = json_obj['email']
    password = json_obj['password']
    print('Register:', email, password)

    # cur = mysql.connection.cursor()
    # cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    # account = cur.fetchone()

    account = Users.query.filter_by(email=email).first()

    if account:
        print('Error: Email already exists!')
        # cur.close()
        emit('register_response', {'message': 'Error: Email already exists!'})
    else:
        # If account doesn't exist, add to database
        # cur.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
        # mysql.connection.commit()
        # cur.close()
        # print('Registration successful!')
        # cur = mysql.connection.cursor()
        # cur.execute('SELECT * FROM confirm_email WHERE email = %s', (email,))
        # account = cur.fetchone()
        account = ConfirmEmail.query.filter_by(email=email).first()

        if account:
            print('Error: Email confirmation code already has been sent!')
            emit('register_response', {'message': 'Email confirmation code already has been sent!'})

        # if account:
        #     print('Error: Email confirmation code already has been sent!')
        #     cur.close()
        #     emit('register_response', {'message': 'Email confirmation code already has been sent!'})

        else:
            # msg = Message('Family Secure', sender='araxmatjonn@gmail.com', recipients=[email])
            code = generate_five_digit_number()
            # msg.body = "Your code: " + str(code)
            # mail.send(msg)
            print("Message sent!")
            emit('register_response', {'message': 'Confirm your Email!'})
            # cur.execute('INSERT INTO confirm_email (email, code) VALUES (%s, %s)', (email, code))
            # mysql.connection.commit()
            # cur.close()
            new_email_confirmation = ConfirmEmail(email=email, code=code)
            db.session.add(new_email_confirmation)
            db.session.commit()
            print('Registration successful!')

    # print('Get data from MySQL')
    # cur = mysql.connection.cursor()u
    # cur.execute('''SELECT * FROM users''')
    # rows = cur.fetchall()
    # for row in rows:
    #     print(f'{row}')
    # cur.close()


@socketio.on('email_confirm')
def handle_my_custom_event_email_confirm(jsonn):
    print('received json: ' + str(jsonn))

    json_obj = json.loads(jsonn)
    email = json_obj['email'].strip()
    email_code = json_obj['email_code'].strip()
    passwd = json_obj['passwd'].strip()

    # cur = mysql.connection.cursor()
    # cur.execute('SELECT email, code FROM confirm_email WHERE email = %s', (email,))
    # result = cur.fetchone()

    email_confirmation = ConfirmEmail.query.filter_by(email=email).first()

    if email_confirmation is not None:
        # result_email = result[0].strip()
        # result_code = str(result[1]).strip()
        result_email = email_confirmation.email.strip()
        result_code = str(email_confirmation.code).strip()
        print(result_email, result_code)

        if result_email == email and result_code == email_code:
            # cur.execute('DELETE FROM confirm_email WHERE email = %s', (email,))
            # mysql.connection.commit()  # Don't forget to commit the changes

            db.session.delete(email_confirmation)
            db.session.commit()

            token = secrets.token_hex(5)

            # cur.execute('INSERT INTO users (email, password, token) VALUES (%s, %s, %s)', (email, passwd, token))
            # mysql.connection.commit()
            # cur.close()

            new_user = Users(email=email, password=passwd,
                             token=token)  # Assuming you have a token field in Users model
            db.session.add(new_user)
            db.session.commit()
            emit('email_confirm_response', {'message': 'Email confirm Success!', 'status': True, 'token': token})

        else:
            emit('email_confirm_response', {'message': 'Incorrect Code!', 'status': False})

        print('received data:', email, email_code)


@socketio.on('user_login')
def handle_my_custom_event_login(jsonn):
    print('received json: ' + str(jsonn))

    json_obj = json.loads(jsonn)
    email = json_obj['email']
    passwd = json_obj['passwd']

    # cur = mysql.connection.cursor()
    # cur.execute('SELECT email, password FROM users WHERE email = %s AND password = %s', (email, passwd,))
    # result = cur.fetchone()

    user = Users.query.filter_by(email=email, password=passwd).first()

    # result_email = result[0]
    # result_passwd = str(result[1])
    # print(result_email, result_passwd)

    if user is not None:
        result_email = user.email
        result_passwd = user.password
        print(result_email, result_passwd)

        if result_email == email and result_passwd == passwd:
            new_token = secrets.token_hex(5)
            # cur.execute('UPDATE users SET token = %s WHERE email = %s AND password = %s',
            #             (new_token, result_email, result_passwd))
            # mysql.connection.commit()

            user.token = new_token
            db.session.commit()
            emit('login_response', {'message': 'Login Success!', 'status': False, 'token': new_token})
            print(new_token)
        else:
            emit('login_response', {'message': 'Login Fail!', 'status': False})
    else:
        emit('login_response', {'message': 'Login Fail!', 'status': False})


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('server_response', {'data': 'Welcome!'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def generate_five_digit_number():
    return random.randint(10000, 99999)


class ConfirmChild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceimei = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(128), nullable=False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(50), nullable=False)


class Childs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceimei = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(50))


class ConfirmEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    code = db.Column(db.Integer)


if __name__ == '__main__':
    socketio.run(app, host='192.168.1.139', port=5000, allow_unsafe_werkzeug=True)
