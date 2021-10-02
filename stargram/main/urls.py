from django.urls import path
from . import views

urlpatterns = [
  path('', views.intro_view, name="intro"),
  path('upload/', views.upload_view, name="upload"),
  path('add_content/', views.add_content, name="add_content"),
  
]
