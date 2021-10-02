from django.shortcuts import render, redirect
from .models import Content, Photo

def intro_view(request):
  return render(request, 'intro.html')

def upload_view(request):
  return render(request, 'upload.html')

