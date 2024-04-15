import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# Getting our dataset
dsPath = r"big_data.csv"
ds = pd.read_csv(dsPath)

# Extracting features
X = ds.drop(columns=["pose","pose_id"])
Y = ds["pose"]

# Assigning each exercise number value
encoder = LabelEncoder()
Y = encoder.fit_transform(Y)

exercise_dic = {
    0: 'overhead',
    1: 'pushup',
    2: 'squat'
}

# Splitting data into train and test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8, shuffle=True, random_state=0)

# Building sequential model
model = tf.keras.Sequential()
shape = (7,)
model.add(tf.keras.layers.Dense(32, activation='relu', input_shape=shape)) # Input layer
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))  # Dropout for regularization
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(3, activation='softmax')) # Output layer

model.compile(optimizer= 'adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])  

# Displays model info
model.summary()

# Fit model with 75 epochs
model.fit(X_train,Y_train,epochs=75,batch_size=32, verbose = 1)

evaluate_val_loss, evaluate_val_acc = model.evaluate(X_test, Y_test)

predict_val = model.predict(X_test)

# Predictions and metrics
predict_val_max = np.argmax(predict_val, axis=1)

# Displaying classification report
print(classification_report(Y_test , predict_val_max, zero_division=0, target_names=encoder.classes_))


# Save model as `exercise_predictor.keras` in current directory.
model.save(r"exercise_predictor.keras")


