from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.db import transaction
import requests
from .models import *
# Create your views here.


class WeatherLocationView():
    
    def get(request):
        if request.method == 'POST':
            
            location_name = request.POST.get('location_name')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            weather_data = WeatherLocation.objects.create(location_name = location_name, latitude = latitude, longitude = longitude)
            weather_data.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return render(request, 'blogs/list weather-location.html', {'weather_locations': WeatherLocation.objects.all()})
    
    def update(request, pk):
        if request.method == 'POST':
        
            weather = WeatherLocation.objects.filter(pk=pk).first()
            weather.location_name = request.POST.get('location_name')
            weather.latitude = request.POST.get('latitude')
            weather.longitude = request.POST.get('longitude')
            weather.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    def delete(request, pk):
        
        weather = WeatherLocation.objects.filter(pk=pk)
        if weather.exists():
            weather.delete()
            return render(request, 'weather_location.html')
        else:
            messages.error(request, 'Weather location does not exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BlogPostView():
    def get(request):
        if request.method == 'POST':
            user = request.user.id
            user_obj = User.objects.filter(id=user).first()
            title = request.POST.get('title')
            content = request.POST.get('content')
            weather_location_id = request.POST.get('weather_location')
            weather_location = WeatherLocation.objects.filter(id=weather_location_id).first()
            
            BlogPost.objects.create(user = user_obj, title = title, content = content, weather_location = weather_location)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        blogs = BlogPost.objects.all()
        context = {'blogs': blogs}
        return render(request, 'blog_post.html', context)    
    
    def update(request, pk):
        blog = BlogPost.objects.filter(pk=pk).first()
        user_id = request.user.id
        user_obj = User.objects.filter(id=user_id).first()
        blog.user = user_obj
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.save()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def delete(request, pk):
        blog = BlogPost.objects.filter(pk=pk)
        if blog.exists():
            blog.delete()
            return render(request, 'blog_post.html')
        else:
            messages.error(request, 'Blog post does not exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class WeatherDataView():
    
    def get(request):
        weather_api_url = "http://api.weatherapi.com/v1/current.json?key=52afd2a44f544e4e9ed200555242604"

        if request.method == 'POST':
            city = request.POST.get('city')
            response = requests.get(weather_api_url + "&q=" + city)
            
            context = {
                'response': response.json()
            }
            return render(request, 'weather_data.html', context)
        
        return render(request, 'weather_data.html')
    }
            