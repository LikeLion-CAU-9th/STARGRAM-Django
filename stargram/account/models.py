from django.db import models
from django.db.models.fields import EmailField

class User_info(models.Model):
  seq = models.AutoField(primary_key=True)
  kakao_id = models.CharField(max_length=30, verbose_name="user_id", default="0")
  email = models.EmailField(max_length=255, verbose_name="user_email", blank = False)
  nickname = models.CharField(max_length=30, verbose_name="user_name")