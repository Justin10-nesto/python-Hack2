from django.contrib import admin
from models import *

admin.site.register(User)
admin.site.register(WeatherLocation)
admin.site.register(Comment)
admin.site.register(BlogPost)
admin.site.register(WeatherData)