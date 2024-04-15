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

"""
Gets the file from the front end to the server for 
processing and prediction. 
"""
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

"""
Gets the processed with body wire frame
and pass it to the front end to display
"""
@app.route('/get_vid', methods=["GET"])
def get_vid():  
    return sf(os.path.join('outputs', 'output.mp4'), mimetype='video/mp4', as_attachment=True)
    
"""
Gets the feedback and pass it to the
front end for display
"""
@app.route('/get_feedback', methods=["GET"])
def get_feedback():
    return sf(os.path.join('outputs', 'feedback.json'))
    

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure upload folder exists
    socketio.run(app, debug=True,port=5001)