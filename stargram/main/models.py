from django.db import models
from account.models import User_info

# Create your models here.
class Card(models.Model):
    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    # user_info = models.ForeignKey(
    #     User_info, on_delete=models.SET_NULL, null=True, blank=True)

    date_start = models.DateField()
    date_end = models.DateField()
    name = models.CharField(max_length=100, null=False, blank=False)
    impression = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    card = models.ForeignKey(
        Card, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="photo/", null=False, blank=False)
    meta = models.TextField(blank=True)
    description = models.TextField()
    
    def __str__(self):
        return self.description