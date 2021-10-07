from django.shortcuts import render, redirect, get_object_or_404
from .models import Card, Photo
from django.core import serializers
from PIL import Image
from PIL.ExifTags import TAGS
import json, folium



def intro_view(request):
  return render(request, 'intro.html')

def upload_view(request):
  return render(request, 'upload.html')

def map_view(request):
  return render(request, 'map.html')

def sketch_view(request, id):
  card= Card.objects.get(id = id)
  photos = Photo.objects.filter(card=card.id)
  
  meta_data=[]
  for photo in photos:
    meta = get_metadata(photo.image.path)
    meta_data.append(meta)
    photo.meta = str(meta)
    photo.save()
  map_mark(meta_data)

  photos = Photo.objects.filter(card=card.id)
  photos_json = serializers.serialize('json', photos)
  print(photos_json)
  return render(request, 'sketch.html', {'photos':photos, 'meta_data':meta_data, 'photos_json':photos_json})


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

    


def get_metadata(img_url):
  
  try:
    
    img = Image.open(img_url)
    
    info = img._getexif()
    exif = {}
    for tag, value in info.items():
      decoded = TAGS.get(tag, tag)
      exif[decoded] = value

    # from the exif data, extract gps
    exifGPS = exif['GPSInfo']
    latData = exifGPS[2]
    lonData = exifGPS[4]

    # calculae the lat / long
    latDeg = latData[0]
    latMin = latData[1]
    latSec = latData[2]
    lonDeg = lonData[0]
    lonMin = lonData[1]
    lonSec = lonData[2]

    # correct the lat/lon based on N/E/W/S
    Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
    if exifGPS[1] == 'S': Lat = Lat * -1
    Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
    if exifGPS[3] == 'W': Lon = Lon * -1

    #getTime
    createTime = info[0x9003]
    Time = createTime[0:4] + "-" + createTime[5:7] + "-" + createTime[8:10] + " " + createTime[11:13] + ":" + createTime[14:16] + ":" + createTime[17:19]

    return {"Lat":Lat, "Lon":Lon, "Time": Time}

  except:
    print('There is no GPS info in this picture')
    return {}


def map_mark(meta_data):

  Lat = meta_data[0]['Lat']
  Lon = meta_data[0]['Lon']
  #first coordination of map
  map = folium.Map(
      location=[Lat, Lon],
      zoom_start=50 #map lever(지도 배율)
  )
  for meta in meta_data:
    Lat = meta['Lat']
    Lon = meta['Lon']
    #add marker on map
    folium.Marker(
        location=[Lat, Lon],
        icon=folium.Icon(color='blue', icon='star')
    ).add_to(map)

  map.save('./main/templates/map.html')