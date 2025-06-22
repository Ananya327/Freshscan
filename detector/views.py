from django.shortcuts import render

# Create your views here.
echo "from django.shortcuts import render

def index(request):
    return render(request, 'index.html')" > detector/views.py
