# README


### Description

In this project, we designed and developed a web application to assist users in their exercises. We created a React web page, in which the user will be able to upload a video (preferably as an .mp4) for analysis. Once uploaded we send the video to our flask server, where we process the video using MediaPipe then pass it through a pre-trained CNN to predict the exercise being completed. After this, using the exercise detected, we provide feedback to correct form based on joint angles calculated within the post processing. To gather data for the project, we used a combination of pre-made video sets and MediaPipe to create the data set our Sequential model is trained on. We found our model achieved an average of 95% accuracy when trained on our data. Once the user submitted video is processed, we pass the type of exercise detected, the feedback and a processed video with body pose wire frames to the front end. All of these will be displayed for the user on the React web page. 


### Self Evaluation

We completed most of what we initially planned on doing within the proposal. We managed to get our exercise predictor working while giving some naive feedback to the user for form optimization.

The following are some changes that we made compared to our proposal
Originally wanted to use openPose for body landmark detection but used Mediapipe instead
Originally wanted to do the 3 exercises as pushups, sit ups, and jumping jacks but instead did overhead press and squats instead of sit ups and jumping jacks
Instead of real-time camera detection, we opted for a video file upload through front end website
Only used a sequential CNN model instead of doing multiple types of models
Built our own dataset based on artificial videos generated by infiniteRep. Pushup data was also gathered through other sources (add more about this?). However our dataset is structured similarly to the “Physical Exercise Recognition Dataset” we mentioned in our proposal


### Instructions / Requirements

Download React version 18.2 (https://nodejs.org/en/download)

Ensure you have Python version 3.11._ (3.11.5, 3.11.7 and 3.11.9 are known to work) (https://www.python.org/downloads/)

Download project file and extract it to directory of your choice

Navigate to server directory using cd in terminal

Execute command “pip install -r requirements.txt” in terminal in order to install project dependencies

The following are the Python pip installs in case requirements.txt fails to install the packages:
>keras
>tensorflow
>mediapipe
>opencv-python
>numpy
>pandas
>scikit-learn

Navigate back to the project directory

React steps:
Installing relevant react packages
>npm i
>npm i axios
In order to run the project, have two separate terminals open. 

In the first terminal, navigate to FormDetection-ML\server directory
Starting server (run command in terminal):
> python server.py 

In the second terminal navigate to FormDetection-ML\client\ml-exercise-trainer directory
Starting client (run command in terminal):
> npm start

Have one terminal running for the client and one terminal for the server.

Please note that our project does not re-train our model each time, rather it uses a saved state of the keras model and predicts based on that. If you wish to retrain the model used for predictions, before starting the server and front end run:
> model_training.py
The output of this file will include the model training as well as classification report


Folder Structure
Entire dataset that we trained our model on is contained in > FormDetection-ML\server/big_data.csv
Our dataset contains 9 columns:
> pose_id relates to each frame analyzed
> pose labels each frame with its associated pose
> the following 7 columns correspond to each of the different joint angles used for training

Our model can be found in 
> FormDetection-ML\server\model_training.py
Our video predictor is found in 
> FormDetection-ML\server/video_predictor.py

Flask backend for our react frontend is found in FormDetection-ML\server/server.py

Feedback and prediction is found in 
> FormDetection-ML\server/outputs
Within this folder, feedback will be within 
> feedback.json
And prediction + mediapipe landmarks will be
> output.mp4

Project directory:

```
FormDetection-ML/
├── client/
│   └── ml-exercise-trainer/
│       ├── node_modules/
│       ├── public/
│       └── src/
│            ├── components/
│            │   └── VideoInput.tsx
│            └── React Files (App.js, App.css, index.css, etc)
├── node_modules/
├── server/
│   ├── server.py
│   ├── exercise_predictor.keras
│   ├── video_predictor.py
│   ├── big_data.csv
│   ├── model_training.py
│   ├── outputs/
│   └── uploads/
└── README.md
```
