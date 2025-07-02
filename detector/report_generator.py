from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import datetime

# Step 1: Nutrition Data with Purpose
nutrition_map = {
    'apple': {
        'calories': 52,
        'protein': '0.3g',
        'vitamin C': '7mg',
        'fiber': '2.4g',
        'sugar': '10g',
        'purpose': 'Boosts immunity and supports heart health.'
    },
    'banana': {
        'calories': 96,
        'protein': '1.3g',
        'vitamin C': '8.7mg',
        'fiber': '2.6g',
        'sugar': '12g',
        'purpose': 'Provides instant energy and supports digestion.'
    },
    'tomato': {
        'calories': 18,
        'protein': '0.9g',
        'vitamin C': '14mg',
        'fiber': '1.2g',
        'sugar': '2.6g',
        'purpose': 'Rich in antioxidants and supports skin health.'
    },
    'carrot': {
        'calories': 41,
        'protein': '0.9g',
        'vitamin A': '835µg',
        'fiber': '2.8g',
        'sugar': '4.7g',
        'purpose': 'Improves eyesight and skin glow.'
    },
    'potato': {
        'calories': 77,
        'protein': '2g',
        'vitamin C': '20mg',
        'fiber': '2.2g',
        'sugar': '1.2g',
        'purpose': 'Provides energy and supports brain health.'
    },
    'cucumber': {
        'calories': 16,
        'protein': '0.7g',
        'vitamin K': '16.4µg',
        'fiber': '0.5g',
        'sugar': '1.7g',
        'purpose': 'Keeps body hydrated and cool.'
    },
    'orange': {
        'calories': 47,
        'protein': '0.9g',
        'vitamin C': '53.2mg',
        'fiber': '2.4g',
        'sugar': '9g',
        'purpose': 'Boosts immune system and refreshes body.'
    },
    'grapes': {
        'calories': 67,
        'protein': '0.6g',
        'vitamin C': '3.2mg',
        'fiber': '0.9g',
        'sugar': '16g',
        'purpose': 'Promotes heart health and reduces inflammation.'
    },
    'mango': {
        'calories': 60,
        'protein': '0.8g',
        'vitamin C': '36.4mg',
        'fiber': '1.6g',
        'sugar': '14g',
        'purpose': 'Improves skin health and boosts immunity.'
    },
    'cherry': {
        'calories': 50,
        'protein': '1g',
        'vitamin C': '7mg',
        'fiber': '1.6g',
        'sugar': '8g',
        'purpose': 'Helps reduce inflammation and improves sleep.'
    }
}

# Step 2: Nutrition lookup function (handles fuzzy match too)
def get_nutrition_info(label):
    label = label.lower().strip()
    for key in nutrition_map:
        if key in label:
            return nutrition_map[key]
    return {'error': 'No nutrition info found for this item.'}

# Step 3: Generate the report
def generate_report(image_path, label, nutrition_data):
    pdf_name = f'detector/static/reports/{label}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    os.makedirs(os.path.dirname(pdf_name), exist_ok=True)

    c = canvas.Canvas(pdf_name, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "FreshScan Detection Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Label: {label.title()}")
    c.drawString(50, 700, f"Calories per 100g: {nutrition_data.get('calories', 'N/A')} kcal")
    c.drawString(50, 680, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Nutrition info block
    c.setFont("Helvetica", 10)
    text_object = c.beginText(50, 640)
    text_object.textLine("Nutrition Info:")
    for key, value in nutrition_data.items():
        if key != 'purpose':
            text_object.textLine(f" - {key.title()}: {value}")
    text_object.textLine("")
    text_object.textLine(f"Purpose: {nutrition_data.get('purpose', 'N/A')}")
    c.drawText(text_object)

    # Attach image if valid
    if os.path.exists(image_path):
        try:
            c.drawImage(image_path, 300, 500, width=200, height=150, preserveAspectRatio=True)
        except Exception:
            pass

    c.showPage()
    c.save()
    return pdf_name
