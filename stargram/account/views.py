from pathlib import Path
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json, os, requests
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_FILE = os.path.join(BASE_DIR, 'secrets.json')


with open(SECRET_FILE) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} env variable.".format(setting)
        raise ImproperlyConfigured(error_msg)

REST_API_KEY = get_secret('KAKAO_REST_KEY')
REDIRECT_URI = "http://localhost:8000/account/login/kakao/callback"
API_HOST = 'https://kauth.kakao.com/oauth/authorize?client_id='+REST_API_KEY+'&redirect_uri='+REDIRECT_URI+'&response_type=code'


def KakaoSignInView(request):
  return redirect(API_HOST)
  
  
def KakaoSignInCallback(request):
  CODE = request.GET['code']
  kakao_token_api = 'https://kauth.kakao.com/oauth/token'
  data = {
    'grant_type': 'authorization_code',
    'client_id': REST_API_KEY,
    'redirection_uri': 'http://localhost:8000/account/login/kakao/callback',
    'code': CODE,
  }
  
  token_response = requests.post(kakao_token_api, data=data)
  access_token = token_response.json().get('access_token')
  user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer {access_token}'})
  user_info_json = user_info_response.json()
  
  user_data = {
    # Dict type data
  }
  
  if 'id' in user_info_json:
    kakao_id = user_info_json['id']
    request.session['kakao_id'] = kakao_id
    user_data['id'] = kakao_id
    
  if 'kakao_account' in user_info_json:
    if 'email' in user_info_json['kakao_account']:
      user_data['email'] = user_info_json['kakao_account']['email']
    if 'nickname' in user_info_json['kakao_account']['profile']:
      user_data['nickname'] = user_info_json['kakao_account']['profile']['nickname']
      
  print(user_data)
    
  return JsonResponse({"user_info": user_info_response.json()})