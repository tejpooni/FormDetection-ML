from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS
from flask import send_from_directory
from flask import send_file as sf
from werkzeug.utils import secure_filename
import os


# app init 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory where files will be stored
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

@app.route('/processed_video/<filename>')
def processed_video(filename):
    """Serve the processed video."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This text was fetched using an HTTP call to server on render'}
    return jsonify(data)

# upload endpoint will acknowledge client (videoUpload component) that it's recv file

@app.route('/send_file', methods=["POST"])
def send_file():
    #file upload 
    ack = {}
    print("Acknowledged")
    try:
        file = request.files['file_uploaded']
        if file:
            file.filename = "videoInput.mp4"
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(f"File {filename} uploaded successfully")
            ack['status'] = 1
            os.system('python video_predictor.py')
            #processed_video("output.mp4", os.path.join(app.config['UPLOAD_FOLDER'], processed_filename))
            return jsonify(status = 1)
        else:
            print("No file part")
            ack['status'] = 0

    except Exception as e:
        print(f"File upload error {e}")
        ack["status"] = 0
    print("Sending ack to server")
    return jsonify(ack);

@app.route('/get_vid', methods=["GET"])
def get_vid():  
    return sf(os.path.join('outputs', 'output.mp4'), mimetype='video/mp4', as_attachment=True)

@app.route('/get_feedback', methods=["GET"])
def get_feedback():
    return sf(os.path.join('outputs', 'feedback.json'))

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ",str(data))
    emit("data",{'data':data,'id':request.sid},broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure upload folder exists
    socketio.run(app, debug=True,port=5001)