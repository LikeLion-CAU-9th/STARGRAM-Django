from django.shortcuts import render, redirect, get_object_or_404
from .models import Card, Photo
from django.core.serializers import json

def intro_view(request):
  return render(request, 'intro.html')

def upload_view(request):
  return render(request, 'upload.html')

def sketch_view(request, id):
  card= Card.objects.get(id = id)
  photos = Photo.objects.filter(card=card.id)
  # json_serializer = json.Serializer()
  # json_photos = json_serializer.serialize(photos)
  return render(request, 'sketch.html', {'photos':photos})

def add_card(request):
  
  if request.method == 'POST':
      data = request.POST
      images = request.FILES.getlist('images')
      card, created = Card.objects.get_or_create(
              date_start=data['date_start'],
              date_end=data['date_end'],
              name=data['place'],
              impression=data['impression']
            )

      for image in images:
          photo = Photo.objects.create(
              card = card,
              description=data['place'],
              image=image,
          )

  return redirect('sketch', card.id)

    