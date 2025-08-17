import os
import pickle
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity

# === CONFIGURATION ===
IMAGE_SIZE = (180, 180)
EMBEDDING_DB_PATH = "detector/detector/embedding_db.pkl"  # Path to saved embeddings
THRESHOLD = 0.75  # Similarity threshold

# === CALORIE MAP ===
calorie_map = {
    'apple': 52, 'banana': 96, 'beetroot': 43, 'bell pepper': 31, 'cabbage': 25,
    'capsicum': 20, 'carrot': 41, 'cauliflower': 25, 'chilli pepper': 40, 'corn': 96,
    'cucumber': 16, 'eggplant': 24, 'garlic': 149, 'ginger': 80, 'grapes': 67,
    'jalepeno': 29, 'kiwi': 61, 'lemon': 29, 'lettuce': 15, 'mango': 60, 'onion': 40,
    'orange': 47, 'paprika': 19, 'pear': 57, 'peas': 81, 'pineapple': 50,
    'pomegranate': 83, 'potato': 77, 'raddish': 16, 'soy beans': 446, 'spinach': 23,
    'sweetcorn': 86, 'sweetpotato': 86, 'tomato': 18, 'turnip': 28, 'watermelon': 30
}

# === LOAD MODEL ONCE ===
print("Loading MobileNetV2 model...")
embedding_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# === LOAD EMBEDDING DATABASE ===
print("Loading embeddings from file...")
with open(EMBEDDING_DB_PATH, 'rb') as f:
    embedding_db = pickle.load(f)

# Convert embeddings to fast lookup arrays
labels = [entry['label'] for entry in embedding_db.values()]
embeddings = np.array([entry['embedding'] for entry in embedding_db.values()])

print(f"Loaded {len(labels)} embeddings.")

# === FUNCTIONS ===
def get_embedding(image_path):
    """Generate embedding for a given image."""
    img = image.load_img(image_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return embedding_model.predict(img_array, verbose=0)[0]

def get_calories(label):
    """Return calorie value for the given label."""
    return calorie_map.get(label.lower(), 0)

def predict_fruit_or_vegetable(image_path):
    """Predict fruit/vegetable label and calories."""
    try:
        query_embedding = get_embedding(image_path)

        # Vectorized similarity (much faster)
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        best_index = np.argmax(similarities)
        best_similarity = similarities[best_index]
        best_label = labels[best_index]

        if best_similarity >= THRESHOLD:
            return best_label, get_calories(best_label), best_similarity
        else:
            return "Not Matching", 0, best_similarity

    except Exception as e:
        return f"Error: {e}", 0, 0


# === EXAMPLE TEST ===
if __name__ == "__main__":
    test_image = r"test_images/apple.jpg"  # Change to your test image path
    label, calories, similarity = predict_fruit_or_vegetable(test_image)
    print(f"Predicted: {label} | Calories: {calories} | Similarity: {similarity:.2f}")
