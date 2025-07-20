# detector/report_generator.py

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import wikipedia

nutrition_map = {
    'apple': {
        'calories': 52, 'carbohydrates': '14g', 'fat': '0.2g', 'protein': '0.3g',
        'fiber': '2.4g', 'vitamins': 'Vitamin C, K', 'purpose': 'Supports heart health and weight loss.'
    },
    'banana': {
        'calories': 96, 'carbohydrates': '27g', 'fat': '0.3g', 'protein': '1.3g',
        'fiber': '2.6g', 'vitamins': 'Vitamin B6, C', 'purpose': 'Provides energy and supports digestion.'
    },
    'beetroot': {
        'calories': 43, 'carbohydrates': '9.6g', 'fat': '0.2g', 'protein': '1.6g',
        'fiber': '2.8g', 'vitamins': 'Vitamin C, Folate', 'purpose': 'Supports blood pressure and stamina.'
    },
    'bell pepper': {
        'calories': 31, 'carbohydrates': '6g', 'fat': '0.3g', 'protein': '1g',
        'fiber': '2.1g', 'vitamins': 'Vitamin C, B6', 'purpose': 'Boosts immunity and eye health.'
    },
    'cabbage': {
        'calories': 25, 'carbohydrates': '6g', 'fat': '0.1g', 'protein': '1.3g',
        'fiber': '2.5g', 'vitamins': 'Vitamin C, K', 'purpose': 'Promotes digestion and reduces inflammation.'
    },
    'capsicum': {
        'calories': 20, 'carbohydrates': '4.7g', 'fat': '0.2g', 'protein': '0.9g',
        'fiber': '1.7g', 'vitamins': 'Vitamin C, A', 'purpose': 'Supports metabolism and immune health.'
    },
    'carrot': {
        'calories': 41, 'carbohydrates': '10g', 'fat': '0.2g', 'protein': '0.9g',
        'fiber': '2.8g', 'vitamins': 'Vitamin A, K1', 'purpose': 'Good for eye health and immunity.'
    },
    'cauliflower': {
        'calories': 25, 'carbohydrates': '5g', 'fat': '0.3g', 'protein': '2g',
        'fiber': '2g', 'vitamins': 'Vitamin C, K', 'purpose': 'Supports digestion and detoxification.'
    },
    'chilli pepper': {
        'calories': 40, 'carbohydrates': '9g', 'fat': '0.4g', 'protein': '2g',
        'fiber': '1.5g', 'vitamins': 'Vitamin C, B6', 'purpose': 'Boosts metabolism and reduces pain.'
    },
    'corn': {
        'calories': 96, 'carbohydrates': '21g', 'fat': '1.5g', 'protein': '3.4g',
        'fiber': '2.7g', 'vitamins': 'Vitamin B3, B5', 'purpose': 'Provides energy and aids digestion.'
    },
    'cucumber': {
        'calories': 16, 'carbohydrates': '3.6g', 'fat': '0.1g', 'protein': '0.7g',
        'fiber': '0.5g', 'vitamins': 'Vitamin K, C', 'purpose': 'Hydrates and supports skin health.'
    },
    'eggplant': {
        'calories': 24, 'carbohydrates': '5.7g', 'fat': '0.2g', 'protein': '1g',
        'fiber': '3g', 'vitamins': 'Vitamin C, B6', 'purpose': 'Lowers cholesterol and supports weight loss.'
    },
    'garlic': {
        'calories': 149, 'carbohydrates': '33g', 'fat': '0.5g', 'protein': '6.4g',
        'fiber': '2.1g', 'vitamins': 'Vitamin C, B6', 'purpose': 'Boosts immunity and reduces blood pressure.'
    },
    'ginger': {
        'calories': 80, 'carbohydrates': '18g', 'fat': '0.8g', 'protein': '1.8g',
        'fiber': '2g', 'vitamins': 'Vitamin B6, C', 'purpose': 'Aids digestion and reduces nausea.'
    },
    'grapes': {
        'calories': 67, 'carbohydrates': '17g', 'fat': '0.4g', 'protein': '0.6g',
        'fiber': '0.9g', 'vitamins': 'Vitamin C, K', 'purpose': 'Supports heart and brain health.'
    },
    'jalepeno': {
        'calories': 29, 'carbohydrates': '6.5g', 'fat': '0.4g', 'protein': '0.9g',
        'fiber': '2.8g', 'vitamins': 'Vitamin C, B6', 'purpose': 'Boosts metabolism and pain relief.'
    },
    'kiwi': {
        'calories': 61, 'carbohydrates': '15g', 'fat': '0.5g', 'protein': '1.1g',
        'fiber': '3g', 'vitamins': 'Vitamin C, K', 'purpose': 'Boosts immunity and digestion.'
    },
    'lemon': {
        'calories': 29, 'carbohydrates': '9.3g', 'fat': '0.3g', 'protein': '1.1g',
        'fiber': '2.8g', 'vitamins': 'Vitamin C, B6', 'purpose': 'Boosts immunity and detoxifies.'
    },
    'lettuce': {
        'calories': 15, 'carbohydrates': '2.9g', 'fat': '0.2g', 'protein': '1.4g',
        'fiber': '1.3g', 'vitamins': 'Vitamin A, K', 'purpose': 'Supports hydration and weight control.'
    },
    'mango': {
        'calories': 60, 'carbohydrates': '15g', 'fat': '0.4g', 'protein': '0.8g',
        'fiber': '1.6g', 'vitamins': 'Vitamin A, C', 'purpose': 'Improves immunity and eye health.'
    },
    'onion': {
        'calories': 40, 'carbohydrates': '9.3g', 'fat': '0.1g', 'protein': '1.1g',
        'fiber': '1.7g', 'vitamins': 'Vitamin C, B6', 'purpose': 'Supports heart health and immunity.'
    },
    'orange': {
        'calories': 47, 'carbohydrates': '12g', 'fat': '0.1g', 'protein': '0.9g',
        'fiber': '2.4g', 'vitamins': 'Vitamin C, B1', 'purpose': 'Boosts immune system and skin health.'
    },
    'paprika': {
        'calories': 19, 'carbohydrates': '4.5g', 'fat': '0.3g', 'protein': '0.9g',
        'fiber': '1.8g', 'vitamins': 'Vitamin A, E', 'purpose': 'Boosts eye health and immune function.'
    },
    'pear': {
        'calories': 57, 'carbohydrates': '15g', 'fat': '0.1g', 'protein': '0.4g',
        'fiber': '3.1g', 'vitamins': 'Vitamin C, K', 'purpose': 'Aids digestion and supports heart health.'
    },
    'peas': {
        'calories': 81, 'carbohydrates': '14g', 'fat': '0.4g', 'protein': '5g',
        'fiber': '5.7g', 'vitamins': 'Vitamin A, K', 'purpose': 'Supports digestion and immunity.'
    },
    'pineapple': {
        'calories': 50, 'carbohydrates': '13g', 'fat': '0.1g', 'protein': '0.5g',
        'fiber': '1.4g', 'vitamins': 'Vitamin C, B1', 'purpose': 'Aids digestion and reduces inflammation.'
    },
    'pomegranate': {
        'calories': 83, 'carbohydrates': '19g', 'fat': '1.2g', 'protein': '1.7g',
        'fiber': '4g', 'vitamins': 'Vitamin C, K', 'purpose': 'Boosts heart health and immunity.'
    },
    'potato': {
        'calories': 77, 'carbohydrates': '17g', 'fat': '0.1g', 'protein': '2g',
        'fiber': '2.2g', 'vitamins': 'Vitamin C, B6', 'purpose': 'Provides energy and supports digestion.'
    },
    'raddish': {
        'calories': 16, 'carbohydrates': '3.4g', 'fat': '0.1g', 'protein': '0.7g',
        'fiber': '1.6g', 'vitamins': 'Vitamin C', 'purpose': 'Supports liver function and digestion.'
    },
    'soy beans': {
        'calories': 446, 'carbohydrates': '30g', 'fat': '20g', 'protein': '36g',
        'fiber': '9.3g', 'vitamins': 'Vitamin K, B9', 'purpose': 'Great source of protein and bone health.'
    },
    'spinach': {
        'calories': 23, 'carbohydrates': '3.6g', 'fat': '0.4g', 'protein': '2.9g',
        'fiber': '2.2g', 'vitamins': 'Vitamin A, C, K', 'purpose': 'Boosts iron levels and vision.'
    },
    'sweetcorn': {
        'calories': 86, 'carbohydrates': '19g', 'fat': '1.2g', 'protein': '3.2g',
        'fiber': '2.7g', 'vitamins': 'Vitamin C, B3', 'purpose': 'Supports digestion and energy.'
    },
    'sweetpotato': {
        'calories': 86, 'carbohydrates': '20g', 'fat': '0.1g', 'protein': '1.6g',
        'fiber': '3g', 'vitamins': 'Vitamin A, C', 'purpose': 'Good for digestion and blood sugar control.'
    },
    'tomato': {
        'calories': 18, 'carbohydrates': '3.9g', 'fat': '0.2g', 'protein': '0.9g',
        'fiber': '1.2g', 'vitamins': 'Vitamin C, K', 'purpose': 'Rich in antioxidants and supports heart health.'
    },
    'turnip': {
        'calories': 28, 'carbohydrates': '6.4g', 'fat': '0.1g', 'protein': '0.9g',
        'fiber': '1.8g', 'vitamins': 'Vitamin C', 'purpose': 'Aids digestion and supports bone health.'
    },
    'watermelon': {
        'calories': 30, 'carbohydrates': '8g', 'fat': '0.2g', 'protein': '0.6g',
        'fiber': '0.4g', 'vitamins': 'Vitamin C, A', 'purpose': 'Hydrating and supports heart health.'
    }
}



def get_nutrition_info(label):
    label = label.lower().strip()
    if label in nutrition_map:
        return nutrition_map[label]
    return {'error': 'No nutrition info found for this item.'}

def get_wikipedia_summary(label):
    try:
        return wikipedia.summary(label, sentences=2)
    except:
        return "Wikipedia info not available."

def generate_report(image_path, label, nutrition_info, fallback_text=None):
    label_clean = label.lower().strip().replace(" ", "_")
    output_path = f"detector/static/reports/{label_clean}_report.pdf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, f"Nutritional Report: {label.title()}")

    if os.path.exists(image_path):
        c.drawImage(ImageReader(image_path), 50, height - 300, width=200, height=200)

    y = height - 320
    c.setFont("Helvetica", 12)

    if fallback_text:
        c.drawString(50, y, "Note: No structured nutrition found. Wikipedia summary:")
        y -= 20
        for line in fallback_text.split('\n'):
            c.drawString(50, y, line)
            y -= 15
    else:
        for key, value in nutrition_info.items():
            if key != 'purpose':
                c.drawString(50, y, f"{key.title()}: {value}")
                y -= 20
        if 'purpose' in nutrition_info:
            y -= 10
            c.drawString(50, y, f"Purpose: {nutrition_info['purpose']}")

    c.save()
    return output_path
