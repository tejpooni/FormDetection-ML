import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


dsPath = r"big_data.csv"
ds = pd.read_csv(dsPath)


X = ds.drop(columns=["pose","pose_id"])  # Features
Y = ds["pose"]

encoder = LabelEncoder()

Y = encoder.fit_transform(Y)

exercise_dic = {
    0: 'overhead',
    1: 'pushup',
    2: 'squat'
}

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8, shuffle=True, random_state=0)

model = tf.keras.Sequential()
shape = (7,)
model.add(tf.keras.layers.Dense(32, activation='relu', input_shape=shape))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))  # Dropout for regularization
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))  # Dropout for regularization
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(3, activation='softmax'))

model.compile(optimizer= 'adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])  

model.summary()

model.fit(X_train,Y_train,epochs=75,batch_size=32, verbose = 1)

evaluate_val_loss, evaluate_val_acc = model.evaluate(X_test, Y_test)

predict_val = model.predict(X_test)

# Predictions and metrics
predict_val_max = np.argmax(predict_val, axis=1)

print(classification_report(Y_test , predict_val_max, zero_division=0, target_names=encoder.classes_))


# Save model as `exercise_predictor.keras`.
model.save(r"exercise_predictor.keras")


