import json
from builtins import print

from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user
from flask_socketio import SocketIO, join_room, leave_room
from db import get_user, change_password, add_user, update_user_info, get_all_doctor, is_doctor
from model import load_our_models, predict_prob, predict_class
from random import seed, randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySecret'
socket_io = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
loaded_model, loaded_tokenizer = load_our_models()
clients = []


@app.route('/', methods=["POST"])
def response():
    message = dict(request.form)['query']
    print(message)
    return jsonify({"response": message})


@app.route('/signup', methods=["POST"])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    phone_number = request.form.get('phone')
    image = request.form.get('image')
    print("name: " + username + " password : " + password + " _phone : " + phone_number)
    add_user(username, password, phone_number, image, False)
    return jsonify({"response": 'done'})


@app.route('/login', methods=["POST"])
def login():
    # if current_user.is_authenticated:
    #     return jsonify({"response": 'is_authenticated'})
    phone = request.form.get('phone')
    print(phone)
    password = request.form.get('password')
    print(password)
    user = get_user(phone)
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"response": user.to_json()})
    return jsonify({"response": 'null'})


@app.route('/check', methods=["POST"])
def check_user():
    phone_number = request.form.get('phone')
    print(phone_number)
    check = get_user(phone_number)
    return jsonify({"response": check.to_json()}) if check else jsonify({"response": 'null'})


@app.route('/reset', methods=["POST"])
def reset_password():
    phone = request.form.get('phone')
    print('new ' + phone + ' password : ' + request.form.get('password'))
    change_password(phone, request.form.get('password'))
    return jsonify({"response": 'done'})


@app.route('/update', methods=["POST"])
def update():
    username = request.form.get('username')
    phone_number = request.form.get('phone')
    image = request.form.get('image')
    print(username + " Update " + phone_number + " image " + image + " AAA ")
    update_user_info(username, phone_number, image)
    return jsonify({"response": 'done'})


@app.route('/logout')
def logout():
    logout()
    return jsonify({"response": 'done'})


@socket_io.on('connect')
def connection():
    print('Connected')


# @socket_io.on('connect')
# def connect():
#     print("a client connected")

@socket_io.on('send_message')
def handle_send_message_event(data):
    print(format(data['username'] + " has sent message to the room " + data['room'] + " : " + data['message']))
    message_data = json.loads(data['message'])
    # user_data = message_data['sender']['phoneNumber']
    # print(user_data)
    print(message_data["text"])
    pred_prob = predict_prob([message_data['text']], loaded_model, loaded_tokenizer)
    the_class = predict_class(pred_prob)

    if pred_prob > 0.5 and not is_doctor(message_data['sender']['phoneNumber']) and not is_doctor(
            message_data['sender']['phoneNumber']):
        doctors = get_all_doctor()
        # print(doctors.count())
        print(doctors[0])
        seed(1)
        index = randint(0, doctors.count() - 1)
        print(index)
        print(doctors[index])
        print(doctors[index]['_phone'])

        data['rate'] = str(int(pred_prob * 100))

        socket_io.emit('receive_message', data, room=doctors[index]['_phone'])

    print('the prob: ' + str(pred_prob))
    print('the class: ' + str(the_class))
    socket_io.emit('receive_message', data, room=data['room'])


@socket_io.on('join_room')
def handle_join_room_event(data):
    print(format(data['username'] + " has joined the room " + data['room']))
    join_room(data['room'])
    socket_io.emit('join_room_announcement', data)


@socket_io.on('leave_room')
def handle_leave_room_event(data):
    print(format(data['username'] + "has left the room " + data['room']))
    leave_room(data['room'])
    socket_io.emit('leave_room_announcement', data, room=data['room'])


#
# @socket_io.on('joined', namespace='/chat')
# def joined(message):
#     clients.append(request.sid)
#
#     room = session.get('room')
#     join_room(room)
#
#     # emit to the first client that joined the room
#     socket_io.emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=clients[0])
#

@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == '__main__':
    socket_io.run(app, host='0.0.0.0')
