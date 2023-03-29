from django.db import models
import geocoder
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
# Create your models here.


class Data(models.Model):
    country = models.CharField(max_length=100, null=True)
    population = models.PositiveIntegerField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Data"

    def save(self, *args, **kwargs):
        self.latitude = geocoder.osm(self.country).lat
        self.longitude = geocoder.osm(self.country).lng
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.country


class Image(models.Model):
    image = models.ImageField(upload_to="images/")

    

class Image2(models.Model):
    image_file = ProcessedImageField(
        upload_to='uploads/',
        processors=[ResizeToFit(width=800, height=600)],
        format='JPEG',
        options={'quality': 60}
        )
    uploaded_at = models.DateTimeField(auto_now_add=True)
