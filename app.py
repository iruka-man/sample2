# OK:50フレームごとに画像データを受信してimgタグに表示する
from flask import Flask, jsonify, render_template;
from flask_socketio import SocketIO, send, emit
import base64

from camera import Camera

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'

@app.route('/')
def index():
    return render_template('index.html')

@socketIo.on("message")
def handleMessage(mes):

    prefix = 'data:image/png;base64,'
    print("koko")

    camera = Camera()
    count = 0
    while True:
        frame = camera.get_frame()
        count += 1

        
        if frame is not None:

            if count % 20 == 0:
                emit('capture-send', { 'dataURL': prefix+base64.b64encode(frame).decode('utf-8')})
        else:
            break

    return None

if __name__ == '__main__':
    socketIo.run(app)
