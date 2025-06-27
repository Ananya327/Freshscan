# detector/report_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from PIL import Image
import os

def generate_report(image_path, label, calories, nutrition_summary=""):
    report_path = "detector/static/report.pdf"
    c = canvas.Canvas(report_path, pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "FreshScan - Fruit & Vegetable Report")

    # Image
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((200, 200))
            img_path_temp = "detector/static/temp_image.jpg"
            img.save(img_path_temp)
            c.drawImage(img_path_temp, 50, 520, width=150, height=150)
        except:
            c.drawString(50, 520, "Image could not be displayed.")

    # Prediction info
    c.setFont("Helvetica", 12)
    c.drawString(50, 480, f"Predicted Label: {label}")
    c.drawString(50, 460, f"Estimated Calories (per 100g): {calories} kcal")
    c.drawString(50, 440, f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Nutrition summary
    if nutrition_summary:
        c.drawString(50, 410, "Nutrition Info (from Wikipedia):")
        text = c.beginText(50, 390)
        text.setFont("Helvetica", 10)
        for line in nutrition_summary.split("\n"):
            text.textLine(line)
        c.drawText(text)

    c.save()
    return report_path
