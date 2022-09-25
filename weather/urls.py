from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from weather.views.API.weather import *

urlpatterns = [
    path('', WeatherListCreateAPIView.as_view()),
	path('<int:pk>', WeatherRetrieveUpdateDestroyAPIView.as_view()), 

]
