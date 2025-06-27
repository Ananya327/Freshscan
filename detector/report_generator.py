# detector/report_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import wikipedia

def generate_pdf(image_path, label, calories, output_path='detector/static/report.pdf'):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "🍎 FreshScan - Prediction Report")

    # Date & Time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Date & Time: {now}")

    # Predicted label
    c.drawString(50, height - 120, f"Prediction: {label}")

    # Calories
    c.drawString(50, height - 140, f"Estimated Calories: {calories} kcal")

    # Nutrition facts (from Wikipedia)
    try:
        summary = wikipedia.summary(label, sentences=2)
        c.drawString(50, height - 180, "Nutrition Info:")
        text_obj = c.beginText(50, height - 200)
        text_obj.setFont("Helvetica", 10)
        for line in summary.split('\n'):
            text_obj.textLine(line)
        c.drawText(text_obj)
    except Exception as e:
        c.drawString(50, height - 180, "Nutrition Info: Not available.")

    # Image
    if os.path.exists(image_path):
        c.drawImage(image_path, 300, height - 300, width=200, preserveAspectRatio=True)

    c.save()
    return output_path
