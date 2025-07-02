# build_embedding_db.py
import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input

# Config
IMAGE_SIZE = (180, 180)
DATA_DIR  = r'D:\FRASHSCAN 1\detector\dataset\Fruits_Vegetables\train'
 # your training folder

# Load pretrained MobileNetV2 model for embeddings
model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

embedding_db = {}

# Walk through all folders and images
for label in os.listdir(DATA_DIR):
    label_path = os.path.join(DATA_DIR, label)
    if not os.path.isdir(label_path):
        continue

    for img_name in os.listdir(label_path):
        img_path = os.path.join(label_path, img_name)
        try:
            img = image.load_img(img_path, target_size=IMAGE_SIZE)
            img_array = image.img_to_array(img)
            img_array = preprocess_input(img_array)
            img_array = np.expand_dims(img_array, axis=0)

            embedding = model.predict(img_array)[0]
            embedding_db[img_path] = {'embedding': embedding, 'label': label}
        except Exception as e:
            print(f"Error with {img_path}: {e}")

# Save database
with open('detector/embedding_db.pkl', 'wb') as f:
    pickle.dump(embedding_db, f)

print(f"Saved {len(embedding_db)} image embeddings.")
