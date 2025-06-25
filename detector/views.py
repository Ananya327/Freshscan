# detector/views.py

from django.shortcuts import render
from .model import predict_fruit_or_vegetable
import os
import uuid

def index(request):
    return render(request, 'index.html')

def result(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        # Ensure unique filename using UUID
        filename = f"{uuid.uuid4().hex}_{image.name}"
        image_path = os.path.join('detector', 'static', filename)

        # Save uploaded image
        with open(image_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Run prediction
        label, calories = predict_fruit_or_vegetable(image_path)

        # Return result to template
        return render(request, 'result.html', {
            'label': label,
            'calories': calories,
            'image_url': '/static/' + filename
        })

    return render(request, 'index.html')
