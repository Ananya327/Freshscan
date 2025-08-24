# detector/report_generator.py

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import wikipedia

nutrition_map = {
    'apple': {
        'calories': 52,
        'carbs': 14,
        'protein': 0.3,
        'fat': 0.2,
        'fiber': 2.4,
        'vitamins': 'Vitamin C, Vitamin K, Potassium',
        'purpose': 'Boosts immunity, aids digestion, supports heart health'
    },
    'banana': {
        'calories': 96,
        'carbs': 27,
        'protein': 1.3,
        'fat': 0.3,
        'fiber': 2.6,
        'vitamins': 'Vitamin B6, Vitamin C, Potassium',
        'purpose': 'Provides energy, supports brain health, aids digestion'
    },
    'bean': {
        'calories': 31,
        'carbs': 7,
        'protein': 2,
        'fat': 0.1,
        'fiber': 3.4,
        'vitamins': 'Vitamin C, Vitamin K, Folate',
        'purpose': 'Supports heart health, improves digestion, rich in fiber'
    },
    'beetroot': {
        'calories': 43,
        'carbs': 10,
        'protein': 1.6,
        'fat': 0.2,
        'fiber': 2.8,
        'vitamins': 'Folate, Vitamin C, Manganese',
        'purpose': 'Improves blood flow, lowers blood pressure, boosts stamina'
    },
    'cabbage': {
        'calories': 25,
        'carbs': 6,
        'protein': 1.3,
        'fat': 0.1,
        'fiber': 2.5,
        'vitamins': 'Vitamin C, Vitamin K, Folate',
        'purpose': 'Supports digestion, reduces inflammation, strengthens immunity'
    },
    'carrot': {
        'calories': 41,
        'carbs': 10,
        'protein': 0.9,
        'fat': 0.2,
        'fiber': 2.8,
        'vitamins': 'Vitamin A, Vitamin K, Potassium',
        'purpose': 'Improves vision, promotes skin health, boosts immunity'
    },
    'cauliflower': {
        'calories': 25,
        'carbs': 5,
        'protein': 2,
        'fat': 0.3,
        'fiber': 2,
        'vitamins': 'Vitamin C, Vitamin K, Folate',
        'purpose': 'Supports weight loss, boosts immunity, improves digestion'
    },
    'cherry': {
        'calories': 50,
        'carbs': 12,
        'protein': 1,
        'fat': 0.3,
        'fiber': 1.6,
        'vitamins': 'Vitamin C, Potassium, Antioxidants',
        'purpose': 'Improves sleep, reduces inflammation, supports heart health'
    },
    'chilli': {
        'calories': 40,
        'carbs': 9,
        'protein': 2,
        'fat': 0.4,
        'fiber': 1.5,
        'vitamins': 'Vitamin C, Vitamin B6, Capsaicin',
        'purpose': 'Boosts metabolism, reduces pain, improves immunity'
    },
    'coriander': {
        'calories': 23,
        'carbs': 4,
        'protein': 2.1,
        'fat': 0.5,
        'fiber': 2.8,
        'vitamins': 'Vitamin C, Vitamin K, Folate',
        'purpose': 'Detoxifies body, aids digestion, reduces blood sugar'
    },
    'ginger root': {
        'calories': 80,
        'carbs': 18,
        'protein': 1.8,
        'fat': 0.8,
        'fiber': 2,
        'vitamins': 'Vitamin C, Magnesium, Potassium',
        'purpose': 'Relieves nausea, reduces inflammation, boosts immunity'
    },
    'grape blue': {
        'calories': 67,
        'carbs': 17,
        'protein': 0.6,
        'fat': 0.4,
        'fiber': 0.9,
        'vitamins': 'Vitamin C, Vitamin K, Antioxidants',
        'purpose': 'Protects heart, improves memory, fights aging'
    },
    'grape white': {
        'calories': 69,
        'carbs': 18,
        'protein': 0.7,
        'fat': 0.2,
        'fiber': 0.9,
        'vitamins': 'Vitamin C, Vitamin K, Antioxidants',
        'purpose': 'Boosts immunity, promotes hydration, supports skin health'
    },
    'guava': {
        'calories': 68,
        'carbs': 14,
        'protein': 2.6,
        'fat': 1,
        'fiber': 5.4,
        'vitamins': 'Vitamin C, Folate, Potassium',
        'purpose': 'Improves digestion, boosts immunity, regulates blood sugar'
    },
    'kiwi': {
        'calories': 61,
        'carbs': 15,
        'protein': 1.1,
        'fat': 0.5,
        'fiber': 3,
        'vitamins': 'Vitamin C, Vitamin K, Vitamin E',
        'purpose': 'Strengthens immunity, aids digestion, improves skin health'
    },
    'lemon': {
        'calories': 29,
        'carbs': 9,
        'protein': 1.1,
        'fat': 0.3,
        'fiber': 2.8,
        'vitamins': 'Vitamin C, Potassium, B-complex',
        'purpose': 'Boosts immunity, detoxifies body, aids digestion'
    },
    'mango': {
        'calories': 60,
        'carbs': 15,
        'protein': 0.8,
        'fat': 0.4,
        'fiber': 1.6,
        'vitamins': 'Vitamin A, Vitamin C, Folate',
        'purpose': 'Improves digestion, boosts immunity, supports eye health'
    },
    'onion': {
        'calories': 40,
        'carbs': 9,
        'protein': 1.1,
        'fat': 0.1,
        'fiber': 1.7,
        'vitamins': 'Vitamin C, Vitamin B6, Folate',
        'purpose': 'Boosts heart health, reduces cholesterol, fights infection'
    },
    'orange': {
        'calories': 47,
        'carbs': 12,
        'protein': 0.9,
        'fat': 0.1,
        'fiber': 2.4,
        'vitamins': 'Vitamin C, Folate, Potassium',
        'purpose': 'Boosts immunity, supports heart health, hydrates body'
    },
    'pineapple': {
        'calories': 50,
        'carbs': 13,
        'protein': 0.5,
        'fat': 0.1,
        'fiber': 1.4,
        'vitamins': 'Vitamin C, Manganese, Bromelain',
        'purpose': 'Aids digestion, boosts immunity, reduces inflammation'
    },
    'pomegranate': {
        'calories': 83,
        'carbs': 19,
        'protein': 1.7,
        'fat': 1.2,
        'fiber': 4,
        'vitamins': 'Vitamin C, Vitamin K, Folate',
        'purpose': 'Improves blood flow, rich in antioxidants, boosts memory'
    },
    'potato': {
        'calories': 77,
        'carbs': 17,
        'protein': 2,
        'fat': 0.1,
        'fiber': 2.2,
        'vitamins': 'Vitamin C, Vitamin B6, Potassium',
        'purpose': 'Provides energy, supports digestion, good for skin health'
    },
    'radish': {
        'calories': 16,
        'carbs': 3.4,
        'protein': 0.7,
        'fat': 0.1,
        'fiber': 1.6,
        'vitamins': 'Vitamin C, Folate, Potassium',
        'purpose': 'Supports liver health, improves digestion, detoxifies body'
    },
    'raspberry': {
        'calories': 52,
        'carbs': 12,
        'protein': 1.2,
        'fat': 0.7,
        'fiber': 6.5,
        'vitamins': 'Vitamin C, Manganese, Fiber',
        'purpose': 'Rich in antioxidants, aids weight loss, improves digestion'
    },
    'strawberry': {
        'calories': 33,
        'carbs': 8,
        'protein': 0.7,
        'fat': 0.3,
        'fiber': 2,
        'vitamins': 'Vitamin C, Manganese, Folate',
        'purpose': 'Boosts immunity, supports skin health, reduces inflammation'
    },
    'tomato': {
        'calories': 18,
        'carbs': 4,
        'protein': 0.9,
        'fat': 0.2,
        'fiber': 1.2,
        'vitamins': 'Vitamin C, Vitamin K, Lycopene',
        'purpose': 'Supports heart health, improves vision, fights cancer cells'
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
