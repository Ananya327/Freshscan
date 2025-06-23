# detector/views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from .model import predict_fruit_or_vegetable
import os

def index(request):
    return render(request, 'index.html')

def detect(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        file_path = fs.path(filename)

        label, calories = predict_fruit_or_vegetable(file_path)

        return render(request, 'result.html', {
            'label': label,
            'calories': calories,
            'image_url': file_url
        })

    return render(request, 'upload.html')
