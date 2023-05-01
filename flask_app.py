from flask import Flask, Response, render_template, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit, join_room
import random
import secrets
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

#generates room for users to be able to chat and watch together
def get_rooms():
    while True:
        room_id = secrets.token_hex(16)
        if room_id not in rooms:
            return room_id

#renders the html files inside the flask app so that the web app will look how intended
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/nav-link')
def nav_link():
    return render_template('code_link.html')

#server side code for both uploading and playing the video that is uploaded
@app.route('/play_video', methods=['POST'])
def play_video():
    video = request.files['video']
    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        video_path = os.path.join('uploads', filename)
        video.save(video_path)
        video_url = url_for('uploaded_file', filename=filename)
        room_id = request.form.get('room_id')
        video_mime = 'video/mp4'
        return render_template('index.html', room_id=room_id, video_url=video_url, video_mime=video_mime, filename=filename)
    else:
        return "File not supported. Please upload a video file."

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@socketio.on('play_video')
def handle_play_video():
    print("Received play_video event")
    emit('play_video', broadcast=True)


@socketio.on('pause_video')
def handle_pause_video():
    emit('pause_video', broadcast=True)


@socketio.on('seek_video')
def handle_seek_video(time):
    emit('seek_video', time, broadcast=True)

allowed_extensions = ['mp4']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return 'No video file found'
    video = request.files['video']
    if video.filename == '':
        return 'No video selected'
    if video and allowed_file(video.filename):
        video.save('static/videos/' + video.filename)
        return render_template('index.html', video_name=video.filename)
    return 'Invalid video file'

#server side code to generate the link for others to join
@app.route('/generate_url')
def generate_url():
    unique_id = secrets.token_hex(16)
    return render_template('code_link.html', unique_id=unique_id)

#creates the watch party
@app.route('/watch_with_others/<room_id>')
def watch_with_others(room_id):
    video_url = rooms[room_id]
    video_mime = 'video/mp4'
    return render_template('index.html', room_id=room_id, video_url=video_url, video_mime=video_mime)

#handles the chat functionality
@socketio.on('send_message')
def handle_send_message(data):
    room_id = data['room_id']
    message = data['message']
    username = data['username']
    join_room(room_id)
    print(f"Received message from user {username} in room {room_id}: {message}")
    emit('receive_message', {'username': username, 'message': message}, room=room_id)


if __name__ == '__main__':
    socketio.run(app, debug=True)