from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
import os

def index(request):
    return render(request, 'index.html')

def detect(request):
    if request.method == 'POST':
        return render(request, 'upload.html')  # Show file upload page

    if request.method == 'GET':
        return HttpResponseRedirect('/')  # If accessed directly, go home

    return HttpResponse("Invalid request.")
