from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .model import predict_fruit_or_vegetable
from .report_generator import get_nutrition_info, get_wikipedia_summary, generate_report
import os
import pillow_avif


def index(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)
        image_path = fs.path(filename)

        label, calories = predict_fruit_or_vegetable(image_path)
        label_key = label.lower().strip()

        if label_key == "not matching":
            # Unrelated image
            nutrition_data = {'error': 'No nutrition info found for this item.'}
            wiki_info = get_wikipedia_summary("unknown fruit or vegetable")
            pdf_path = generate_report(image_path, label, {}, fallback_text=wiki_info)
        else:
            # Matched item
            nutrition_data = get_nutrition_info(label_key)

            if 'error' in nutrition_data:
                # No structured data found; fallback to Wikipedia
                wiki_info = get_wikipedia_summary(label)
                pdf_path = generate_report(image_path, label, {}, fallback_text=wiki_info)
            else:
                # Structured data found; use it in report
                pdf_path = generate_report(image_path, label, nutrition_data)

        return render(request, 'index.html', {
            'label': label.title(),
            'label_key': label_key,
            'calories': calories,
            'image_url': image_url,
            'nutrition_info': nutrition_data,
            'pdf_url': pdf_path.replace('detector/static', '/static') if pdf_path else None
        })

    return render(request, 'index.html')
