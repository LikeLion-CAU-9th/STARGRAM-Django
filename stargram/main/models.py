from django.db import models

# Create your models here.
class Content(models.Model):
    class Meta:
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'

    # user = models.ForeignKey(
    #     User, on_delete=models.SET_NULL, null=True, blank=True)

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
    
    content = models.ForeignKey(
        Content, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()
    
    def __str__(self):
        return self.description