from django.shortcuts import render, redirect
from .models import Content, Photo

def intro_view(request):
  return render(request, 'intro.html')

def upload_view(request):
  return render(request, 'upload.html')

def add_content(request):
  
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        content, created = Content.objects.get_or_create(
                date_start=data['date_start'],
                date_end=data['date_end'],
                name=data['place'],
                impression=data['impression']
              )

        for image in images:
            photo = Photo.objects.create(
                content = content,
                description=data['place'],
                image=image,
            )

    return redirect('intro')

    