import os
import pickle
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, classification_report

# ==============================
# CONFIGURATION
# ==============================
IMAGE_SIZE = (224, 224)   # must match embedding.py
EMBEDDING_DB_PATH = "detector/detector/embedding_db.pkl"  # fixed path (avoid double detector)
THRESHOLD = 0.65  # Similarity threshold → if lower than this, mark as "not matching"
TEST_DATASET_PATH = r"D:\FRASHSCAN 1 - Copy\detector\dataset\Fruits_Vegetables\test"

# ==============================
# CALORIE MAP
# ==============================
calorie_map = {
    'apple': 52, 'banana': 96, 'bean': 31, 'beetroot': 43, 'cabbage': 25,
    'carrot': 41, 'cauliflower': 25, 'cherry': 50, 'chilli': 40, 'coriander': 23,
    'ginger root': 80, 'grape blue': 67, 'grape white': 69, 'guava': 68,
    'kiwi': 61, 'lemon': 29, 'mango': 60, 'onion': 40, 'orange': 47,
    'pineapple': 50, 'pomegranate': 83, 'potato': 77, 'radish': 16,
    'raspberry': 52, 'strawberry': 33, 'tomato': 18
}

# ==============================
# LOAD MODEL
# ==============================
print("Loading MobileNetV2 model...")
embedding_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# ==============================
# LOAD EMBEDDING DATABASE
# ==============================
print("Loading embeddings from file...")
with open(EMBEDDING_DB_PATH, 'rb') as f:
    embedding_db = pickle.load(f)

labels = [entry['label'] for entry in embedding_db.values()]
embeddings = np.array([entry['embedding'] for entry in embedding_db.values()])
print(f"✅ Loaded {len(labels)} embeddings.")

# ==============================
# FUNCTIONS
# ==============================
def get_embedding(image_path):
    """Generate embedding for a given image."""
    img = image.load_img(image_path, target_size=IMAGE_SIZE).convert("RGB")
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return embedding_model.predict(img_array, verbose=0)[0]

def get_calories(label):
    return calorie_map.get(label.lower(), 0)

def predict_fruit_or_vegetable(image_path):
    """Predict fruit/vegetable for a given image."""
    try:
        query_embedding = get_embedding(image_path)
        similarities = cosine_similarity([query_embedding], embeddings)[0]

        # Prevent cheating: ignore identical cosine=1 matches
        similarities = np.where(similarities >= 0.9999, 0, similarities)

        best_index = np.argmax(similarities)
        best_similarity = similarities[best_index]
        best_label = labels[best_index]

        if best_similarity >= THRESHOLD:
            return best_label.lower(), get_calories(best_label), best_similarity
        else:
            return "not matching", 0, best_similarity

    except Exception as e:
        return f"error: {e}", 0, 0

def evaluate_accuracy():
    """Evaluate accuracy on test dataset."""
    y_true, y_pred = [], []

    for class_name in os.listdir(TEST_DATASET_PATH):
        class_folder = os.path.join(TEST_DATASET_PATH, class_name)
        if not os.path.isdir(class_folder):
            continue

        for img_file in os.listdir(class_folder):
            img_path = os.path.join(class_folder, img_file)
            pred_label, _, _ = predict_fruit_or_vegetable(img_path)

            y_true.append(class_name.lower())
            y_pred.append(pred_label.lower())

    y_pred_cleaned = [p if p != "not matching" else "unknown" for p in y_pred]

    acc = accuracy_score(y_true, y_pred_cleaned)
    print("\n=== MODEL EVALUATION ===")
    print(f"Accuracy (with 'unknown' counted): {acc:.2f}")
    print("\nClassification Report:\n", classification_report(y_true, y_pred_cleaned))

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    test_image = r"test_images/apple.jpg"  # Change path if needed
    label, calories, similarity = predict_fruit_or_vegetable(test_image)
    print(f"Predicted: {label} | Calories: {calories} | Similarity: {similarity:.2f}")

    evaluate_accuracy()
