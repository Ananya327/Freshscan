# detector/views.py

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .model import predict_fruit_or_vegetable

def index(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        # Call prediction function
        full_image_path = fs.path(filename)
        label, calories = predict_fruit_or_vegetable(full_image_path)

        context = {
            'uploaded_file_url': uploaded_file_url,
            'label': label,
            'calories': calories,
        }

    return render(request, 'index.html', context)
