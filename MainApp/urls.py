

from django.urls import path
from . import views

urlpatterns = [
    path('weather/location/', views.WeatherLocationView.get, name='weather_location'),
    path('weather/location/edit/<str:pk>', views.WeatherLocationView.update, name='weather_location_edit'),
    path('weather/location/delete/<str:pk>', views.WeatherLocationView.delete, name='weather_location_delete'),
    
    path('weather/blogs/', views.BlogPostView.get, name='blog_post'),
    path('weather/blogs/edit/<str:pk>', views.BlogPostView.update, name='blog_post_edit'),
    path('weather/blogs/delete/<str:pk>', views.BlogPostView.delete, name='blog_post_delete'),
    
    path('weather/data', views.WeatherDataView.get, name='weather_data')
    
    
    
]
