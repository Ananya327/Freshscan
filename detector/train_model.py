# detector/model.py

import cv2
import numpy as np
import tensorflow as tf
import pickle
import os

# Load model and labels once at the top
MODEL_PATH = os.path.join("detector", "trained_model", "model.h5")
LABELS_PATH = os.path.join("detector", "trained_model", "labels.pkl")

model = tf.keras.models.load_model(MODEL_PATH)

with open(LABELS_PATH, "rb") as f:
    label_map = pickle.load(f)

# Reverse the label map for predictions
index_to_label = {v: k for k, v in label_map.items()}

# Dummy calories (replace with actual if needed)
calorie_map = {label: 50 + i * 10 for i, label in enumerate(label_map)}

def predict_fruit_or_vegetable(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return "Unknown", 0

    img = cv2.resize(img, (100, 100))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)  # (1, 100, 100, 3)

    predictions = model.predict(img)
    predicted_class = np.argmax(predictions[0])
    label = index_to_label[predicted_class]
    calories = calorie_map.get(label, 0)

    return label, calories
