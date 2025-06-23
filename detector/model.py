# detector/model.py
import cv2
import random

def predict_fruit_or_vegetable(image_path):
    """
    Simulate basic object detection using image analysis.
    Currently picks a random label. To be replaced with ML logic later.
    """
    labels = ['Apple', 'Banana', 'Tomato', 'Carrot', 'Potato']
    calories = {
        'Apple': 52,
        'Banana': 96,
        'Tomato': 18,
        'Carrot': 41,
        'Potato': 77,
    }

    # Load the image using OpenCV (for future ML/model use)
    image = cv2.imread(image_path)

    # Optional basic image checks (for logs/debug)
    if image is None:
        return "Unknown", 0

    # For now: random prediction
    prediction = random.choice(labels)
    return prediction, calories[prediction]
