from chroma_db import *
import time
import threading
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# In-memory storage for messages and client UUIDs
messages = []
client_uuids = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post_message', methods=['POST'])
def post_message():
    data = request.json
    message = data.get('message')
    if message:
        messages.append(message)
        # Emit the message to all connected WebSocket clients
        socketio.emit('new_message', {'message': message})
        return jsonify({'status': 'Message received'}), 200
    return jsonify({'error': 'No message provided'}), 400

@app.route('/load_data', methods=['GET'])
def load_data():
    return jsonify({'messages': messages}), 200

@app.route('/view')
def serve_index():
    return send_from_directory('templates', 'index.html')

@app.route('/view/:file')
def serve_files(file):
    return send_from_directory('templates', file)

@socketio.event
def my_event(message):
    emit('my response', {'data': 'got it!'})

@socketio.on('connect')
def handle_connect():
    client_uuid = str(uuid.uuid4())
    client_uuids[request.sid] = client_uuid
    print(f'Client connected: {client_uuid}')
    # Send all previous messages to the newly connected client
    for message in messages:
        emit('new_message', {'message': message})
    emit('assign_uuid', {'uuid': client_uuid})

@socketio.on('disconnect')
def handle_disconnect():
    client_uuid = client_uuids.pop(request.sid, None)
    print(f'Client disconnected: {client_uuid}')

def send_uuid_to_clients():
    while True:
        socketio.sleep(5)
        for sid, client_uuid in client_uuids.items():
            socketio.emit('uuid_update', {'uuid': client_uuid}, room=sid)

if __name__ == '__main__':
    # Start the background task
    socketio.start_background_task(send_uuid_to_clients)
    socketio.run(app, host="0.0.0.0", debug=True)

