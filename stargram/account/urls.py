from django.urls import path
from . import views

urlpatterns = [
  path('login/kakao', views.KakaoSignInView, name="kakao_signin"),
  path('login/kakao/callback', views.KakaoSignInCallback, name="kakao_signin"),
]
