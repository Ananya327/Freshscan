import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
import numpy as np
import pickle

IMAGE_SIZE = (180, 180)
DATA_DIR = r'D:\FRASHSCAN 1\detector\dataset\Fruits_Vegetables\train'

model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
embedding_db = {}

print("Looking in:", DATA_DIR)
print("Folders found:", os.listdir(DATA_DIR))

for label in os.listdir(DATA_DIR):
    label_path = os.path.join(DATA_DIR, label)
    if not os.path.isdir(label_path):
        continue

    print(f"\nProcessing label: {label}")

    for img_name in os.listdir(label_path):
        img_path = os.path.join(label_path, img_name)
        try:
            print("  →", img_name)
            img = image.load_img(img_path, target_size=IMAGE_SIZE).convert("RGB")
            img_array = image.img_to_array(img)
            img_array = preprocess_input(img_array)
            img_array = np.expand_dims(img_array, axis=0)

            embedding = model.predict(img_array, verbose=0)[0]
            embedding_db[img_path] = {'embedding': embedding, 'label': label}

        except Exception as e:
            print(f"  [Error] {img_name}: {e}")

# ✅ Ensure 'detector/' directory exists before saving
os.makedirs('detector', exist_ok=True)

# Save after processing
with open('detector/embedding_db.pkl', 'wb') as f:
    pickle.dump(embedding_db, f)

print(f"\n✅ Done. Saved {len(embedding_db)} image embeddings.")
