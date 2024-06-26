import keras
import pandas as pd
import numpy as np
import tensorflow as tf
import cv2
import mediapipe as mp
import math
import os
import random as r
import json

class OwnLandmark:
    def __init__(self, x,y):
        self.x = x
        self.y = y


def write_feedback(exercise, feedback):
    # Data to be written
    dictionary = {
        "feedback": f"Exercise: {exercise} \n Feedback: {feedback}"
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=2)
    # Writing to sample.json
    with open(os.path.join("outputs", "feedback.json"), "w") as outfile:
        outfile.write(json_object)


"""
    list of angles:
        0: right_wrist_right_elbow_right_shoulder
        1: left_wrist_left_elbow_left_shoulder
        2: right_elbow_right_shoulder_right_hip
        3: left_elbow_left_shoulder_left_hip
        4: left_shoulder_left_hip_left_ankle
        5: right_shoulder_right_hip_right_ankle
"""
def pushup(list_of_angles):
    list_of_angles[0] = abs(list_of_angles[0])
    list_of_angles[1] = abs(list_of_angles[1])
    list_of_angles[2] = abs(list_of_angles[2])
    list_of_angles[3] = abs(list_of_angles[3])
    list_of_angles[4] = abs(list_of_angles[4])
    list_of_angles[5] = abs(list_of_angles[5])

    global feedback_pu
    global SUCCESS

    elbow_angle = (list_of_angles[0] + list_of_angles[1]) / 2
    body_angle = (list_of_angles[4] + list_of_angles[5]) / 2

    if (70 <= elbow_angle <= 100) and (160 <= body_angle <= 200):
        SUCCESS = True
    else:
        
        if elbow_angle < 70:
            if not "90 deg" in feedback_pu:
                feedback_pu += " You went too low; your elbows should be at 90 deg"
        if elbow_angle > 100:
            if not "90 deg" in feedback_pu:
                feedback_pu += " You didn't go low enough; your elbows should be at 90 deg"
        
        if body_angle < 160:
            if not "hips" in feedback_pu:
                feedback_pu += " Try lowering your hips so your body appears linear"
        if body_angle > 200:
            if not "hips" in feedback_pu:
                feedback_pu += " Push your hips up so that your body is in a straight line"
    return


"""
    0: left_hip_left_knee_left_ankle
    1: right_hip_right_knee_right_ankle
"""
def squat(list_of_angles):

    avg_knee = (list_of_angles[0] + list_of_angles[1])/2
    global feedback_sq
    global SUCCESS

    if 75 > avg_knee:
        if not SUCCESS:
            SUCCESS = False
            feedback_sq = "You are going too low! "
    elif  75 <= avg_knee and avg_knee <= 100:
        SUCCESS = True
    else:
        if not "too" in feedback_sq:
            feedback_sq = "You need to go lower!"


"""
    0: left_wrist_left_elbow_left_shoulder
    1: right_wrist_right_elbow_right_shoulder
    2: left_elbow_left_shoulder_left_hip
    3: right_elbow_right_shoulder_right_hip
"""
def overhead(list_of_angles):
    global feedback_oh
    global SUCCESS

    if (160 < list_of_angles[0] or 160 < list_of_angles[1]) and (160 < list_of_angles[2] or 160 < list_of_angles[3]):
        if not "arms" in feedback_oh:
            feedback_oh += "Try raising your arms higher (they should approach 180 degrees)"
    elif 80 > list_of_angles[0] or 80 > list_of_angles[1]:
        if not "elbow" in feedback_oh:
            feedback_oh += "elbow bad (closer to 90 degrees)"
        SUCCESS = False
    else:
        SUCCESS = True
    
"""
a, b, c, are coordinates in the form of tuples  
with x & y being its first & second elements.
"""
def find_angle(a,b,c):
  radians = np.arctan2(c.y-b.y, c.x-b.x) - np.arctan2(a.y-b.y, a.x-b.x)
  return radians * (180/math.pi)


"""
Draws label on cv2 window
"""
def __draw_label(img, text, pos, bg_color):
   font_face = cv2.FONT_HERSHEY_SIMPLEX
   scale = 2
   color = (0, 0, 0)
   thickness = cv2.FILLED
   margin = 2
   txt_size = cv2.getTextSize(text, font_face, scale, thickness)

   end_x = pos[0] + txt_size[0][0] + margin
   end_y = pos[1] - txt_size[0][1] - margin

   cv2.rectangle(img, pos, (end_x+2, end_y+2), bg_color, thickness)
   cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)


exercise_id = {
    0 : 'overhead'     ,
    1 : 'pushups'      , 
    2 : 'squats'
}

SUCCESS = False 
feedback_sq = ""
feedback_pu = ""
feedback_oh = ""
frame_ids = [0,0,0]

# Retreieve saved model
model = keras.models.load_model(r"exercise_predictor.keras")

# Checks for video uploaded through front end (Supports mp4 and mov file types)
for f in os.listdir("uploads"):
    print(f)
    if str(f).endswith(".mp4"):
        user_input = os.path.join("uploads", "videoInput.mp4")
    elif str(f).endswith(".mov"):
        user_input = os.path.join("uploads", "videoInput.mov")
    else:
        print("No filetype supported")
        os._exit(0)

# Processes video
cap = cv2.VideoCapture(user_input)
width = int(cap.get(3))
height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')

# Build new video
output_path = os.path.join('outputs', 'output.mp4')
out = cv2.VideoWriter(output_path, fourcc, 20.0, (width,height))

#Check if camera was opened correctly
if not (cap.isOpened()):
    print("Could not open video device")

# Pre-trained pose estimation model from Google Mediapipe
mp_pose = mp.solutions.pose

# Supported Mediapipe visualization tools
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# List to store pose landmarks for each frame
pose_landmarks_list = []

# fetch one frame at a time from input video and predict using model
while cap.isOpened():
    
    # frame is a numpy array, that you can predict on 
    ret, frame = cap.read()

    # Check if a frame was successfully read
    if not ret:
        print("Error: Failed to read frame from the video. / End of video reached.")
        break

    # Check if the frame is empty
    if frame is None:
        print("Error: Empty frame received.")
        continue


    imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)

    # Draw landmarks on the image
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    else: # Cannot detect landmark
        continue

    # Extract pose landmarks for the current frame
    pose_landmarks = []
    pose_landmarks_list = []
    if results.pose_landmarks:
        # Calculating x y values for mid hip
        mid_hip_x = (results.pose_landmarks.landmark[24].x + results.pose_landmarks.landmark[23].x)/2
        mid_hip_y = (results.pose_landmarks.landmark[24].y + results.pose_landmarks.landmark[23].y)/2
        mid_hip = OwnLandmark(mid_hip_x, mid_hip_y)

        # Calculate different angles based on landmarks
        right_elbow_right_shoulder_right_hip    = find_angle(results.pose_landmarks.landmark[14], results.pose_landmarks.landmark[12], results.pose_landmarks.landmark[24])
        left_elbow_left_shoulder_left_hip       = find_angle(results.pose_landmarks.landmark[13], results.pose_landmarks.landmark[11], results.pose_landmarks.landmark[23])
        right_knee_mid_hip_left_knee            = find_angle(results.pose_landmarks.landmark[26], mid_hip, results.pose_landmarks.landmark[25])
        right_hip_right_knee_right_ankle        = find_angle(results.pose_landmarks.landmark[24], results.pose_landmarks.landmark[26], results.pose_landmarks.landmark[28])
        left_hip_left_knee_left_ankle           = find_angle(results.pose_landmarks.landmark[23], results.pose_landmarks.landmark[25], results.pose_landmarks.landmark[27])
        right_wrist_right_elbow_right_shoulder  = find_angle(results.pose_landmarks.landmark[16], results.pose_landmarks.landmark[14], results.pose_landmarks.landmark[12])
        left_wrist_left_elbow_left_shoulder     = find_angle(results.pose_landmarks.landmark[15], results.pose_landmarks.landmark[13], results.pose_landmarks.landmark[11]) 
        left_shoulder_left_hip_left_ankle       = find_angle(results.pose_landmarks.landmark[11], results.pose_landmarks.landmark[23], results.pose_landmarks.landmark[27])
        right_shoulder_right_hip_right_ankle    = find_angle(results.pose_landmarks.landmark[12], results.pose_landmarks.landmark[24], results.pose_landmarks.landmark[28])

        # Storing angles
        pose_landmarks.append(right_elbow_right_shoulder_right_hip)
        pose_landmarks.append(left_elbow_left_shoulder_left_hip)
        pose_landmarks.append(right_knee_mid_hip_left_knee)
        pose_landmarks.append(right_hip_right_knee_right_ankle)
        pose_landmarks.append(left_hip_left_knee_left_ankle)
        pose_landmarks.append(right_wrist_right_elbow_right_shoulder)
        pose_landmarks.append(left_wrist_left_elbow_left_shoulder)

    # Append the pose landmarks to the list
    pose_landmarks_list.append(pose_landmarks)

    # Convert pose landmarks list to numpy array
    pose_landmarks_array = np.array(pose_landmarks_list)

    # Predict video frame using model
    prediction = model.predict(pose_landmarks_array)

    predicted_class = np.argmax(prediction, axis=-1)

    # Adding the label on the cv2 frame
    __draw_label(frame, 'Label: {}'.format(exercise_id[predicted_class[0]]), (40,40), (255,255,255))

    # Feedback section
    frame_ids[predicted_class[0]] += 1

    # Generates feedback based on exercise
    if predicted_class[0] == 0: # Overhead Press
        overhead([left_wrist_left_elbow_left_shoulder, right_wrist_right_elbow_right_shoulder, 
                  left_elbow_left_shoulder_left_hip, right_elbow_right_shoulder_right_hip])
        print(SUCCESS)
    elif predicted_class[0] == 1: # Pushups
        pushup([right_wrist_right_elbow_right_shoulder, left_wrist_left_elbow_left_shoulder, right_elbow_right_shoulder_right_hip,
                left_elbow_left_shoulder_left_hip, left_shoulder_left_hip_left_ankle, right_shoulder_right_hip_right_ankle])
        print(SUCCESS)
    elif predicted_class[0] == 2: # Squats
        squat([left_hip_left_knee_left_ankle, right_hip_right_knee_right_ankle])
        print(SUCCESS)
        

    # Writes the frame to new video
    out.write(frame)
   
    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Gets the most detected exercise based on all frame predictions
ex = np.argmax(frame_ids)

# If perfect form detected
if SUCCESS:
    success_list = ["Good Job!", "Nice Work!", "Keep it up!", "Great Effort!", "Fantastic job!"] 
    feedback = "Good form, " + r.choice(success_list)
    write_feedback(exercise_id[ex], feedback)
    print(feedback)
else: # Improper form
    if ex == 0: # Overhead
        write_feedback(exercise_id[ex], feedback_oh)
        print(feedback_oh)
    elif ex == 1: # Pushups
        write_feedback(exercise_id[ex], feedback_pu)
        print(feedback_pu)
    else: # Squats
        write_feedback(exercise_id[ex], feedback_sq)
        print(feedback_sq)

# When everything done, release the capture
out.release()
cap.release()
cv2.destroyAllWindows()