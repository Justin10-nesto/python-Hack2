from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class WeatherLocation(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True,
                           default=uuid4)
    location_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location_name
    
    class Meta:
        verbose_name = 'Weather Location'
        verbose_name_plural = 'Weather Location'

class BlogPost(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True,
                           default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    weather_location = models.ForeignKey(WeatherLocation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Post'


class Comment(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True,
                           default=uuid4)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment_text
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class WeatherData(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True,
                           default=uuid4)
    location = models.ForeignKey(WeatherLocation, on_delete=models.CASCADE)
    date = models.DateField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    precipitation = models.DecimalField(max_digits=5, decimal_places=2)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.location.location_name} - {self.date}"
    
    class Meta:
        verbose_name = 'Weather Data'
        verbose_name_plural = 'Weather Data'
