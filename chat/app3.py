#coding:UTF-8
from flask import Flask, render_template, session, request,flash,redirect,url_for
from flask_socketio import SocketIO, emit,join_room,leave_room,rooms,send
import urllib
from datetime import timedelta

app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'secret!'
ROOM = ['狗蛋','猪头']
num = 0

socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index3.html')


# @socketio.on('client_event')
# def client_msg(msg):
#     message = urllib.parse.unquote(msg['data'])
#     emit('server_response', {'data': message})


@socketio.on('connect_event')
def connected_msg(msg):
    message = urllib.parse.unquote(msg['data'])
    emit('server_response', {'data': message})

@socketio.on('message')
def connected_msg(msg):
    print(request.sid)
    message = urllib.parse.unquote(msg['data'])
    send({"name1":session['user'],"data1":message},room=session['room'])


@socketio.on('join')
def on_join(data):
    room = urllib.parse.unquote(data['room'])
    username = urllib.parse.unquote(data['username'])
    print("room: " + room + ', username: ' + username)
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
    session['user'] = username
    session['room'] = room
    join_room(room)
    send({"name1":session['user'],"data1":' 我来啦！！！'} ,room=room)



@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')