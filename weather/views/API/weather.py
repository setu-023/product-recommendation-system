import json
import re
from urllib import request
from django.conf import settings

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
import requests
import json

from weather.serializers import WeatherSerializer
from weather.models import Weather
from weather.permission import *


class WeatherListCreateAPIView(ListCreateAPIView):
    
    serializer_class = WeatherSerializer
    queryset = Weather.objects.filter()
    permission_classes = [CustomePermission,]

    def create(self, request, *args, **kwargs):

        serializer = WeatherSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'201', 'msg': 'created successfully', 'data':serializer.data, }, status.HTTP_201_CREATED,)
        return Response({'status':'400', 'msg': 'Please Insert Correct value', 'data':serializer.errors, }, status.HTTP_400_BAD_REQUEST,)  
       
    def list(self, request):

        queryset = self.get_queryset()
        serializer = WeatherSerializer(queryset, many=True)
        return Response({ "response": status.HTTP_200_OK,"message":"showing data","data":serializer.data}) 



class WeatherRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = WeatherSerializer
    queryset = Weather.objects.all()
    permission_classes = [CustomePermission,]
    lookup_field = 'pk'


    def get(self, request, pk, *args, **kwargs):
        try:
            weather              = Weather.objects.get(id=pk)
            serializer           = WeatherSerializer(weather)
        except Exception as e:
            return Response({'status':'404', 'msg': str(e) }, status.HTTP_404_NOT_FOUND,)  

        return Response({'status':'200', 'msg': 'showing data', 'data':serializer.data, }, status.HTTP_200_OK,)
   
    def put(self,request,pk,format=None):

        try:
            weather        = Weather.objects.get(id=pk)
            serializer  = WeatherSerializer(weather, data=request.data, partial = True)

        except Exception as e:
            return Response({'status':'404', 'msg': str(e) }, status.HTTP_404_NOT_FOUND,)  

        if serializer.is_valid():
            serializer.save()
            return Response({'status':'200', 'msg': 'data updated', 'data':serializer.data, }, status.HTTP_200_OK,)
        return Response({'status':'400', 'msg': 'Please Insert Correct value', 'data':serializer.errors, }, status.HTTP_400_BAD_REQUEST,)  


    def delete(self,request,pk,format=None):
        try:
            weather        = Weather.objects.get(id=pk)
        except Exception as e:
            return Response({'status':'404', 'msg': str(e) }, status.HTTP_404_NOT_FOUND,)  

        weather.delete()
        return Response({'status':'200', 'msg': 'data deleted', }, status.HTTP_200_OK,)

  
def get_current_temp(request):
        
        try:
            ##get current temp by lat & lon
            # get_response = requests.get("https://api.openweathermap.org/data/2.5/weather?units=metric&lat=24.363588&lon=88.624138&appid=82a0819c96f416ad31782a78f046d871")
            ##get current temp by city name
            get_response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=dhaka&units=metric&appid=82a0819c96f416ad31782a78f046d871")

            print(get_response.text)
            get_current_temp = json.loads(get_response.text)
            get_current_temp = get_current_temp['main']['temp']
            get_weather_type = Weather.objects.get(low_range__lte=get_current_temp, high_range__gte=get_current_temp)
            print((get_weather_type))
            get_weather_type_id = WeatherSerializer(get_weather_type)
            print(get_weather_type_id.data['name'])

        except Exception as e:
            print(e)
            return None
        return get_weather_type_id.data['name']