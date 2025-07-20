# test_predict.py

from model import predict_fruit_or_vegetable

# Replace this with the correct path to a test image
test_image_path = "dataset/Fruits_Vegetables/test/mango/test_1.jpg"  # ← adjust as needed

label, calories = predict_fruit_or_vegetable(test_image_path)

print("Prediction:", label)
print("Estimated Calories:", calories)
