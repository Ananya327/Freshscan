# detector/model.py

import cv2
import numpy as np
import tensorflow as tf
import pickle

# Load trained model and label map
model = tf.keras.models.load_model("detector/trained_model/model.h5")
with open("detector/trained_model/labels.pkl", "rb") as f:
    label_map = pickle.load(f)

# Reverse label map: {0: 'Apple', ...}
rev_label_map = {v: k for k, v in label_map.items()}

# Calorie values (example – customize if needed)
calories = {
    'Apple': 52,
    'Banana': 96,
    'Tomato': 18,
    'Carrot': 41,
    'Potato': 77,
    # Add more if needed
}

def predict_fruit_or_vegetable(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return "Invalid image", 0

    img = cv2.resize(img, (100, 100))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img)
    predicted_index = np.argmax(predictions)
    predicted_label = list(label_map.keys())[list(label_map.values()).index(predicted_index)]

    calorie = calories.get(predicted_label, 0)
    return predicted_label, calorie

