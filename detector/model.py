# detector/model.py

import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity

# === CONFIGURATION ===
IMAGE_SIZE = (180, 180)
EMBEDDING_DB_PATH = "detector/detector/embedding_db.pkl"
 # Path to your generated .pkl file
THRESHOLD = 0.70 # Cosine similarity threshold for determining a match

# === CALORIE MAP ===
calorie_map = {
    'apple': 52,
    'banana': 96,
    'beetroot': 43,
    'bell pepper': 31,
    'cabbage': 25,
    'capsicum': 20,
    'carrot': 41,
    'cauliflower': 25,
    'chilli pepper': 40,
    'corn': 96,
    'cucumber': 16,
    'eggplant': 24,
    'garlic': 149,
    'ginger': 80,
    'grapes': 67,
    'jalepeno': 29,
    'kiwi': 61,
    'lemon': 29,
    'lettuce': 15,
    'mango': 60,
    'onion': 40,
    'orange': 47,
    'paprika': 19,
    'pear': 57,
    'peas': 81,
    'pineapple': 50,
    'pomegranate': 83,
    'potato': 77,
    'raddish': 16,
    'soy beans': 446,
    'spinach': 23,
    'sweetcorn': 86,
    'sweetpotato': 86,
    'tomato': 18,
    'turnip': 28,
    'watermelon': 30
}

# === LOAD EMBEDDING MODEL ===
embedding_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# === LOAD EMBEDDING DATABASE ===
with open(EMBEDDING_DB_PATH, 'rb') as f:
    embedding_db = pickle.load(f)


# === FUNCTION: Get Embedding from Uploaded Image ===
def get_embedding(image_path):
    img = image.load_img(image_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    embedding = embedding_model.predict(img_array, verbose=0)[0]
    return embedding


# === FUNCTION: Get Calories from Label ===
def get_calories(label):
    label = label.lower()
    return calorie_map.get(label, 0)


# === FUNCTION: Predict Fruit or Vegetable ===
def predict_fruit_or_vegetable(image_path):
    try:
        query_embedding = get_embedding(image_path)

        best_similarity = -1
        best_label = None

        for entry in embedding_db.values():
            similarity = cosine_similarity(
                [query_embedding], [entry['embedding']]
            )[0][0]

            if similarity > best_similarity:
                best_similarity = similarity
                best_label = entry['label']

        # Determine match based on similarity threshold
        if best_similarity >= THRESHOLD:
            calories = get_calories(best_label)
            return best_label, calories
        else:
            return "Not Matching", 0

    except Exception as e:
        return f"Error: {e}", 0




