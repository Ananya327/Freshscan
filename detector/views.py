from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from .model import predict_fruit_or_vegetable
import os

def index(request):
    return render(request, 'index.html')

def detect(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)

        # Predict using dummy model
        prediction, calorie = predict_fruit_or_vegetable(fs.path(filename))

        return render(request, 'result.html', {
            'image_url': image_url,
            'prediction': prediction,
            'calorie': calorie
        })
    return render(request, 'upload.html')
